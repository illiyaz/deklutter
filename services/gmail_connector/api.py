import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import OAuthToken, MailDecisionLog
from services.gateway.deps import CurrentUser
from services.gmail_connector.oauth import _fernet, get_gmail_service
from services.classifier.policy import classify_bulk

logger = logging.getLogger(__name__)

def _get_token(db: Session, user: CurrentUser) -> OAuthToken | None:
    return db.query(OAuthToken).filter(OAuthToken.user_id==user.user_id, OAuthToken.provider=="google").order_by(OAuthToken.id.desc()).first()

def scan_recent(user: CurrentUser, days_back: int, limit: int, db: Session = next(get_db())):
    tok = _get_token(db, user)
    if not tok: return {"error":"not_authorized"}
    f = _fernet()
    service = get_gmail_service(f.decrypt(tok.access_token).decode(), f.decrypt(tok.refresh_token).decode() or None, tok.expiry)

    logger.info(f"Scanning Gmail for user_id={user.user_id}, days_back={days_back}, limit={limit}")
    
    msgs_meta = []
    resp = service.users().messages().list(userId="me", maxResults=min(100, limit)).execute()
    
    ids = [m["id"] for m in resp.get("messages", [])]
    logger.info(f"Found {len(ids)} messages for user_id={user.user_id}")
    for mid in ids:
        m = service.users().messages().get(userId="me", id=mid, format="metadata", metadataHeaders=["Subject","From","Date"]).execute()
        size = m.get("sizeEstimate", 0)
        labels = m.get("labelIds", [])
        headers = {h["name"]:h["value"] for h in m.get("payload",{}).get("headers",[])}
        msgs_meta.append({
            "id": mid,
            "from": headers.get("From",""),
            "subject": headers.get("Subject",""),
            "date": headers.get("Date",""),
            "labels": labels,
            "size": size
        })

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
    
    return {
        "summary": plan["summary"],
        "safe_to_delete": [i["id"] for i in plan["items"] if i["decision"]=="delete"],
        "review": [i["id"] for i in plan["items"] if i["decision"]=="review"],
        "keep": [i["id"] for i in plan["items"] if i["decision"]=="keep"],
        "samples": samples
    }

def apply_cleanup(user: CurrentUser, message_ids: list[str], mode: str, db: Session = next(get_db())):
    tok = _get_token(db, user)
    if not tok: return {"error":"not_authorized"}
    f = _fernet()
    service = get_gmail_service(f.decrypt(tok.access_token).decode(), f.decrypt(tok.refresh_token).decode() or None, tok.expiry)

    if mode == "trash":
        # move to Trash (undo possible in Gmail)
        for mid in message_ids:
            service.users().messages().trash(userId="me", id=mid).execute()
    else:
        # label only - create label if it doesn't exist
        label_name = "Deklutter_Review"
        
        # Get existing labels
        labels_response = service.users().labels().list(userId="me").execute()
        existing_labels = {label['name']: label['id'] for label in labels_response.get('labels', [])}
        
        # Create label if it doesn't exist
        if label_name not in existing_labels:
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            created_label = service.users().labels().create(userId="me", body=label_object).execute()
            label_id = created_label['id']
            logger.info(f"Created label '{label_name}' with ID: {label_id}")
        else:
            label_id = existing_labels[label_name]
        
        # Apply label to messages
        for mid in message_ids:
            service.users().messages().modify(userId="me", id=mid, body={"addLabelIds":[label_id]}).execute()

    # mark applied
    db.query(MailDecisionLog).filter(MailDecisionLog.user_id==user.user_id, MailDecisionLog.message_id.in_(message_ids)).update({"applied": True}, synchronize_session=False)
    db.commit()
    return {"deleted": len(message_ids) if mode=="trash" else 0, "labeled": len(message_ids) if mode!="trash" else 0}