"""
Gmail connector implementation using the BaseConnector interface.
"""

import os
import base64
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from cryptography.fernet import Fernet
import requests

from services.connectors.base import BaseConnector, ProviderType, ItemCategory
from db.models import OAuthToken, MailDecisionLog
from services.classifier.policy import classify_bulk

logger = logging.getLogger(__name__)


class GmailConnector(BaseConnector):
    """Gmail email connector"""
    
    SCOPES_READONLY = ["https://www.googleapis.com/auth/gmail.readonly"]
    SCOPES_MODIFY = ["https://www.googleapis.com/auth/gmail.modify"]
    
    def __init__(self):
        super().__init__(ProviderType.EMAIL_GMAIL)
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    
    def _get_fernet(self):
        """Get Fernet encryption instance"""
        key = base64.urlsafe_b64encode((os.getenv("APP_SECRET", "change-me") * 2)[:32].encode())
        return Fernet(key)
    
    def _get_token(self, user_id: int, db) -> Optional[OAuthToken]:
        """Get OAuth token for user"""
        return db.query(OAuthToken).filter(
            OAuthToken.user_id == user_id,
            OAuthToken.provider == "google"
        ).order_by(OAuthToken.id.desc()).first()
    
    def _get_gmail_service(self, access_token: str, refresh_token: Optional[str], expiry: Optional[datetime]):
        """Create Gmail API service"""
        creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        return build("gmail", "v1", credentials=creds, cache_discovery=False)
    
    def get_oauth_url(self, user_email: str, state: Optional[str] = None) -> str:
        """Generate Gmail OAuth URL"""
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uris": [self.redirect_uri],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            scopes=self.SCOPES_READONLY
        )
        flow.redirect_uri = self.redirect_uri
        
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
            state=state or f"user:{user_email}"
        )
        
        return auth_url
    
    def exchange_code_for_tokens(self, code: str, user_id: int, db) -> bool:
        """Exchange authorization code for tokens"""
        try:
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code"
            }
            
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            # Extract tokens
            access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token", "")
            expires_in = token_data.get("expires_in", 3600)
            granted_scope = token_data.get("scope", " ".join(self.SCOPES_READONLY))
            
            # Calculate expiry
            expiry = datetime.utcnow() + timedelta(seconds=expires_in)
            
            # Encrypt and store tokens
            f = self._get_fernet()
            tok = OAuthToken(
                user_id=user_id,
                provider="google",
                scope=granted_scope,
                access_token=f.encrypt(access_token.encode()),
                refresh_token=f.encrypt(refresh_token.encode()) if refresh_token else b"",
                expiry=expiry
            )
            db.add(tok)
            db.commit()
            
            logger.info(f"Gmail OAuth tokens stored for user_id={user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Gmail OAuth token exchange failed for user_id={user_id}: {str(e)}")
            raise
    
    def scan_items(
        self,
        user_id: int,
        db,
        days_back: int = 30,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Scan Gmail inbox for emails"""
        tok = self._get_token(user_id, db)
        if not tok:
            raise ValueError("Gmail not authorized. Please complete OAuth flow.")
        
        # Decrypt tokens
        f = self._get_fernet()
        access_token = f.decrypt(tok.access_token).decode()
        refresh_token = f.decrypt(tok.refresh_token).decode() if tok.refresh_token else None
        
        # Get Gmail service
        service = self._get_gmail_service(access_token, refresh_token, tok.expiry)
        
        logger.info(f"Scanning Gmail for user_id={user_id}, days_back={days_back}, limit={limit}")
        
        # Fetch messages
        msgs_meta = []
        resp = service.users().messages().list(userId="me", maxResults=min(100, limit)).execute()
        
        ids = [m["id"] for m in resp.get("messages", [])]
        logger.info(f"Found {len(ids)} messages for user_id={user_id}")
        
        for mid in ids:
            m = service.users().messages().get(
                userId="me",
                id=mid,
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"]
            ).execute()
            
            size = m.get("sizeEstimate", 0)
            labels = m.get("labelIds", [])
            headers = {h["name"]: h["value"] for h in m.get("payload", {}).get("headers", [])}
            
            msgs_meta.append({
                "id": mid,
                "from": headers.get("From", ""),
                "subject": headers.get("Subject", ""),
                "date": headers.get("Date", ""),
                "labels": labels,
                "size": size
            })
        
        # Classify emails
        plan = classify_bulk(msgs_meta)
        
        # Persist preview log
        for it in plan["items"]:
            db.add(MailDecisionLog(
                user_id=user_id,
                message_id=it["id"],
                sender_hash=it["sender_hash"],
                subject=it["subject"][:500],
                size_bytes=it["size"],
                proposed=it["decision"],
                confidence=int(it["confidence"] * 100)
            ))
        db.commit()
        
        # Return standardized format
        return {
            "summary": {
                "total_items": plan["summary"]["total_items"],
                "counts": plan["summary"]["counts"],
                "total_size_mb": plan["summary"]["approx_size_mb"]
            },
            "items": {
                "delete": [i["id"] for i in plan["items"] if i["decision"] == "delete"],
                "review": [i["id"] for i in plan["items"] if i["decision"] == "review"],
                "keep": [i["id"] for i in plan["items"] if i["decision"] == "keep"]
            },
            "metadata": {
                "provider": "gmail",
                "scan_time": datetime.utcnow().isoformat(),
                "filters_applied": filters or {}
            }
        }
    
    def apply_action(
        self,
        user_id: int,
        db,
        item_ids: List[str],
        action: str = "delete"
    ) -> Dict[str, Any]:
        """Apply action to Gmail messages"""
        tok = self._get_token(user_id, db)
        if not tok:
            raise ValueError("Gmail not authorized")
        
        # Decrypt tokens
        f = self._get_fernet()
        access_token = f.decrypt(tok.access_token).decode()
        refresh_token = f.decrypt(tok.refresh_token).decode() if tok.refresh_token else None
        
        # Get Gmail service
        service = self._get_gmail_service(access_token, refresh_token, tok.expiry)
        
        processed = 0
        failed = 0
        errors = []
        
        try:
            if action == "delete" or action == "trash":
                # Move to trash (recoverable)
                for mid in item_ids:
                    try:
                        service.users().messages().trash(userId="me", id=mid).execute()
                        processed += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"Failed to trash {mid}: {str(e)}")
            
            elif action == "label":
                # Add label
                label_id = "Deklutter_Review"
                for mid in item_ids:
                    try:
                        service.users().messages().modify(
                            userId="me",
                            id=mid,
                            body={"addLabelIds": [label_id]}
                        ).execute()
                        processed += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"Failed to label {mid}: {str(e)}")
            
            # Mark as applied in database
            db.query(MailDecisionLog).filter(
                MailDecisionLog.user_id == user_id,
                MailDecisionLog.message_id.in_(item_ids)
            ).update({"applied": True}, synchronize_session=False)
            db.commit()
            
            logger.info(f"Applied {action} to {processed} emails for user_id={user_id}")
            
            return {
                "success": failed == 0,
                "processed": processed,
                "failed": failed,
                "action": action,
                "errors": errors
            }
            
        except Exception as e:
            logger.error(f"Failed to apply action for user_id={user_id}: {str(e)}")
            return {
                "success": False,
                "processed": processed,
                "failed": len(item_ids) - processed,
                "action": action,
                "errors": [str(e)]
            }
    
    def get_item_details(
        self,
        user_id: int,
        db,
        item_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """Get detailed information about emails"""
        tok = self._get_token(user_id, db)
        if not tok:
            raise ValueError("Gmail not authorized")
        
        # Decrypt tokens
        f = self._get_fernet()
        access_token = f.decrypt(tok.access_token).decode()
        refresh_token = f.decrypt(tok.refresh_token).decode() if tok.refresh_token else None
        
        # Get Gmail service
        service = self._get_gmail_service(access_token, refresh_token, tok.expiry)
        
        details = []
        for mid in item_ids:
            try:
                m = service.users().messages().get(userId="me", id=mid, format="full").execute()
                headers = {h["name"]: h["value"] for h in m.get("payload", {}).get("headers", [])}
                
                details.append({
                    "id": mid,
                    "from": headers.get("From", ""),
                    "to": headers.get("To", ""),
                    "subject": headers.get("Subject", ""),
                    "date": headers.get("Date", ""),
                    "size": m.get("sizeEstimate", 0),
                    "labels": m.get("labelIds", []),
                    "snippet": m.get("snippet", "")
                })
            except Exception as e:
                logger.error(f"Failed to get details for {mid}: {str(e)}")
        
        return details
    
    def revoke_access(self, user_id: int, db) -> bool:
        """Revoke Gmail OAuth access"""
        try:
            tok = self._get_token(user_id, db)
            if tok:
                db.delete(tok)
                db.commit()
                logger.info(f"Revoked Gmail access for user_id={user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to revoke Gmail access for user_id={user_id}: {str(e)}")
            return False
    
    def _get_supported_features(self) -> List[str]:
        """Gmail supported features"""
        return ["scan", "delete", "trash", "label", "oauth", "details"]
