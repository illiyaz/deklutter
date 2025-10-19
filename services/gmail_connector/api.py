import logging
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import OAuthToken, MailDecisionLog
from services.gateway.deps import CurrentUser
from services.gmail_connector.oauth import _fernet, get_gmail_service
from services.classifier.policy import classify_bulk
from googleapiclient.errors import HttpError
from services.gmail_connector.circuit_breaker import get_circuit_breaker, CircuitBreakerOpenError
from services.connectors.provider_config import get_provider_config

logger = logging.getLogger(__name__)

# Load Gmail-specific configuration
GMAIL_CONFIG = get_provider_config("gmail")

# Get circuit breaker for Gmail API
gmail_circuit_breaker = get_circuit_breaker(
    "gmail_api",
    failure_threshold=GMAIL_CONFIG.circuit_breaker_failure_threshold,
    timeout=GMAIL_CONFIG.circuit_breaker_timeout,
    success_threshold=GMAIL_CONFIG.circuit_breaker_success_threshold
)

# Gmail API rate limiting (from provider config)
MAX_EMAILS_PER_SCAN = GMAIL_CONFIG.max_emails_per_scan
BATCH_SIZE = GMAIL_CONFIG.batch_size
RATE_LIMIT_DELAY = GMAIL_CONFIG.rate_limit_delay
MAX_RETRIES = GMAIL_CONFIG.max_retries
RETRY_DELAY = GMAIL_CONFIG.retry_delay
RETRY_STATUS_CODES = GMAIL_CONFIG.retry_on_status_codes

def _retry_with_backoff(func, max_retries=MAX_RETRIES, operation_name="API call", use_circuit_breaker=True):
    """
    Retry a function with exponential backoff for transient failures
    Integrates with circuit breaker pattern
    """
    for attempt in range(max_retries):
        try:
            # Wrap with circuit breaker if enabled
            if use_circuit_breaker:
                return gmail_circuit_breaker.call(func)
            else:
                return func()
                
        except CircuitBreakerOpenError as e:
            # Circuit breaker is open, don't retry
            logger.error(f"{operation_name}: Circuit breaker is OPEN, aborting")
            raise
            
        except HttpError as e:
            status_code = e.resp.status
            
            # Retry on transient errors (configured per provider)
            if status_code in RETRY_STATUS_CODES and attempt < max_retries - 1:
                wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                logger.warning(f"{operation_name} failed with {status_code}, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            
            # Don't retry on client errors (400, 401, 403, 404)
            logger.error(f"{operation_name} failed with status {status_code}: {str(e)}")
            raise
            
        except Exception as e:
            # Retry on network errors
            if attempt < max_retries - 1:
                wait_time = RETRY_DELAY * (2 ** attempt)
                logger.warning(f"{operation_name} failed with {type(e).__name__}: {str(e)}, retrying in {wait_time}s")
                time.sleep(wait_time)
                continue
            
            logger.error(f"{operation_name} failed after {max_retries} attempts: {str(e)}")
            raise
    
    raise Exception(f"{operation_name} failed after {max_retries} retries")

def _get_token(db: Session, user: CurrentUser) -> OAuthToken | None:
    return db.query(OAuthToken).filter(OAuthToken.user_id==user.user_id, OAuthToken.provider=="google").order_by(OAuthToken.id.desc()).first()

def scan_recent(user: CurrentUser, days_back: int, limit: int, db: Session = next(get_db())):
    tok = _get_token(db, user)
    if not tok: return {"error":"not_authorized"}
    f = _fernet()
    service = get_gmail_service(f.decrypt(tok.access_token).decode(), f.decrypt(tok.refresh_token).decode() or None, tok.expiry)

    logger.info(f"Scanning Gmail for user_id={user.user_id}, days_back={days_back}, limit={limit}")
    
    # Cap limit to prevent overwhelming API and user
    effective_limit = min(limit, MAX_EMAILS_PER_SCAN)
    if limit > MAX_EMAILS_PER_SCAN:
        logger.warning(f"Limit {limit} exceeds max {MAX_EMAILS_PER_SCAN}, capping to {MAX_EMAILS_PER_SCAN}")
    
    # Step 1: Get message IDs with pagination
    all_ids = []
    page_token = None
    
    try:
        while len(all_ids) < effective_limit:
            batch_size = min(100, effective_limit - len(all_ids))
            list_params = {
                "userId": "me",
                "maxResults": batch_size
            }
            if page_token:
                list_params["pageToken"] = page_token
            
            # Wrap API call with retry logic
            def list_messages():
                return service.users().messages().list(**list_params).execute()
            
            resp = _retry_with_backoff(list_messages, operation_name=f"List messages (page {len(all_ids)//100 + 1})")
            messages = resp.get("messages", [])
            
            if not messages:
                break
            
            all_ids.extend([m["id"] for m in messages])
            page_token = resp.get("nextPageToken")
            
            if not page_token:
                break
            
            logger.info(f"Fetched {len(all_ids)} message IDs so far...")
    except CircuitBreakerOpenError as e:
        logger.error(f"Circuit breaker open for user_id={user.user_id}: {str(e)}")
        return {"error": "service_unavailable", "message": "Gmail API is temporarily unavailable. Please try again in a minute."}
    except Exception as e:
        logger.error(f"Failed to list messages for user_id={user.user_id}: {str(e)}")
        return {"error": "scan_failed", "message": "Failed to fetch email list. Please try again."}
    
    logger.info(f"Found {len(all_ids)} total messages for user_id={user.user_id}")
    
    # Step 2: Fetch metadata in batches (much faster!)
    msgs_meta = []
    failed_batches = 0
    
    for i in range(0, len(all_ids), BATCH_SIZE):
        batch_ids = all_ids[i:i + BATCH_SIZE]
        logger.info(f"Fetching metadata batch {i//BATCH_SIZE + 1}/{(len(all_ids)-1)//BATCH_SIZE + 1} ({len(batch_ids)} emails)")
        
        try:
            # Use batch request for efficiency
            batch = service.new_batch_http_request()
            
            def create_callback(message_id):
                def callback(request_id, response, exception):
                    if exception:
                        logger.error(f"Error fetching message {message_id}: {exception}")
                        return
                    
                    size = response.get("sizeEstimate", 0)
                    labels = response.get("labelIds", [])
                    headers = {h["name"]:h["value"] for h in response.get("payload",{}).get("headers",[])}
                    msgs_meta.append({
                        "id": message_id,
                        "from": headers.get("From",""),
                        "subject": headers.get("Subject",""),
                        "date": headers.get("Date",""),
                        "labels": labels,
                        "size": size
                    })
                return callback
            
            for mid in batch_ids:
                batch.add(
                    service.users().messages().get(
                        userId="me", 
                        id=mid, 
                        format="metadata", 
                        metadataHeaders=["Subject","From","Date"]
                    ),
                    callback=create_callback(mid)
                )
            
            # Wrap batch execution with retry
            def execute_batch():
                return batch.execute()
            
            _retry_with_backoff(execute_batch, operation_name=f"Fetch metadata batch {i//BATCH_SIZE + 1}")
            
            # Small delay to respect rate limits
            if i + BATCH_SIZE < len(all_ids):
                time.sleep(RATE_LIMIT_DELAY)
                
        except Exception as e:
            failed_batches += 1
            logger.error(f"Failed to fetch batch {i//BATCH_SIZE + 1}: {str(e)}")
            # Continue with next batch instead of failing completely
            if failed_batches > 3:  # Too many failures
                logger.error(f"Too many batch failures ({failed_batches}), aborting scan")
                return {"error": "scan_failed", "message": "Failed to fetch email metadata. Please try again."}
    
    logger.info(f"Successfully fetched metadata for {len(msgs_meta)} emails")

    plan = classify_bulk(msgs_meta)
    
    # Create a mapping of message_id to metadata for easy lookup
    msg_lookup = {m["id"]: m for m in msgs_meta}
    
    # persist preview log (not applied)
    for it in plan["items"]:
        db.add(MailDecisionLog(
            user_id=user.user_id,
            message_id=it["id"],
            sender_hash=it["sender_hash"],
            subject=it["subject"][:500],
            size_bytes=it["size"],
            proposed=it["decision"],
            confidence=int(it["confidence"]*100)
        ))
    db.commit()
    
    # Helper function to get sample emails for a category
    def get_samples(items, category, max_samples=5):
        category_items = [i for i in items if i["decision"] == category]
        samples = []
        for item in category_items[:max_samples]:
            msg_meta = msg_lookup.get(item["id"])
            if msg_meta:
                samples.append({
                    "from": msg_meta["from"],
                    "subject": msg_meta["subject"],
                    "date": msg_meta["date"],
                    "size_kb": round(msg_meta["size"] / 1024, 1)
                })
        return samples
    
    # Get sample emails for each category
    samples = {
        "delete": get_samples(plan["items"], "delete", 5),
        "review": get_samples(plan["items"], "review", 3),
        "keep": get_samples(plan["items"], "keep", 3)
    }
    
    result = {
        "summary": plan["summary"],
        "safe_to_delete": [i["id"] for i in plan["items"] if i["decision"]=="delete"],
        "review": [i["id"] for i in plan["items"] if i["decision"]=="review"],
        "keep": [i["id"] for i in plan["items"] if i["decision"]=="keep"],
        "samples": samples,
        "scanned_count": len(all_ids),
        "hit_limit": len(all_ids) >= effective_limit
    }
    
    return result

def apply_cleanup(user: CurrentUser, message_ids: list[str], mode: str, db: Session = next(get_db())):
    tok = _get_token(db, user)
    if not tok: return {"error":"not_authorized"}
    f = _fernet()
    service = get_gmail_service(f.decrypt(tok.access_token).decode(), f.decrypt(tok.refresh_token).decode() or None, tok.expiry)

    logger.info(f"Applying cleanup for user_id={user.user_id}, mode={mode}, count={len(message_ids)}")
    
    try:
        if mode == "trash":
            # move to Trash (undo possible in Gmail)
            failed_count = 0
            for mid in message_ids:
                try:
                    def trash_message():
                        return service.users().messages().trash(userId="me", id=mid).execute()
                    
                    _retry_with_backoff(trash_message, operation_name=f"Trash message {mid}")
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to trash message {mid}: {str(e)}")
                    if failed_count > 5:  # Too many failures
                        logger.error(f"Too many failures ({failed_count}), aborting cleanup")
                        return {"error": "cleanup_failed", "message": "Failed to delete some emails. Please try again."}
            
            if failed_count > 0:
                logger.warning(f"Cleanup completed with {failed_count} failures out of {len(message_ids)}")
        else:
            # label only - create label if it doesn't exist
            label_name = "Deklutter_Review"
            
            # Get existing labels with retry
            def list_labels():
                return service.users().labels().list(userId="me").execute()
            
            labels_response = _retry_with_backoff(list_labels, operation_name="List labels")
            existing_labels = {label['name']: label['id'] for label in labels_response.get('labels', [])}
            
            # Create label if it doesn't exist
            if label_name not in existing_labels:
                label_object = {
                    'name': label_name,
                    'labelListVisibility': 'labelShow',
                    'messageListVisibility': 'show'
                }
                
                def create_label():
                    return service.users().labels().create(userId="me", body=label_object).execute()
                
                created_label = _retry_with_backoff(create_label, operation_name="Create label")
                label_id = created_label['id']
                logger.info(f"Created label '{label_name}' with ID: {label_id}")
            else:
                label_id = existing_labels[label_name]
            
            # Apply label to messages
            failed_count = 0
            for mid in message_ids:
                try:
                    def modify_message():
                        return service.users().messages().modify(userId="me", id=mid, body={"addLabelIds":[label_id]}).execute()
                    
                    _retry_with_backoff(modify_message, operation_name=f"Label message {mid}")
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to label message {mid}: {str(e)}")
                    if failed_count > 5:
                        logger.error(f"Too many failures ({failed_count}), aborting labeling")
                        return {"error": "cleanup_failed", "message": "Failed to label some emails. Please try again."}

        # mark applied
        db.query(MailDecisionLog).filter(MailDecisionLog.user_id==user.user_id, MailDecisionLog.message_id.in_(message_ids)).update({"applied": True}, synchronize_session=False)
        db.commit()
        
        logger.info(f"Cleanup completed successfully for user_id={user.user_id}")
        return {"deleted": len(message_ids) if mode=="trash" else 0, "labeled": len(message_ids) if mode!="trash" else 0}
        
    except Exception as e:
        logger.error(f"Cleanup failed for user_id={user.user_id}: {str(e)}")
        return {"error": "cleanup_failed", "message": "Failed to complete cleanup. Please try again."}