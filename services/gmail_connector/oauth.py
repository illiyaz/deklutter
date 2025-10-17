import os
import base64
import logging
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from db.models import OAuthToken
from cryptography.fernet import Fernet
from services.gateway.deps import CurrentUser

logger = logging.getLogger(__name__)

_SCOPES_READONLY = ["https://www.googleapis.com/auth/gmail.readonly"]
_SCOPES_MODIFY   = ["https://www.googleapis.com/auth/gmail.modify"]

def _fernet():
    key = base64.urlsafe_b64encode((os.getenv("APP_SECRET","change-me")*2)[:32].encode())
    return Fernet(key)

def get_google_auth_url(readonly: bool, state: str | None = None) -> str:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    scopes = _SCOPES_READONLY if readonly else _SCOPES_MODIFY
    flow = Flow.from_client_config(
        {"web":{"client_id":client_id,"client_secret":client_secret,"redirect_uris":[redirect_uri],"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token"}},
        scopes=scopes
    )
    flow.redirect_uri = redirect_uri
    auth_url, _ = flow.authorization_url(access_type="offline", include_granted_scopes="true", prompt="consent", state=state)
    return auth_url

def exchange_code_store_tokens(code: str, user: CurrentUser, db, scopes: list[str] | None = None) -> bool:
    try:
        import requests
        
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        
        # Exchange code for tokens directly without scope validation
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        token_data = response.json()
        
        # Extract tokens
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token", "")
        expires_in = token_data.get("expires_in", 3600)
        granted_scope = token_data.get("scope", " ".join(_SCOPES_READONLY))
        
        # Calculate expiry
        expiry = datetime.utcnow() + timedelta(seconds=expires_in)
        
        # Encrypt and store tokens
        f = _fernet()
        tok = OAuthToken(
            user_id=user.user_id,
            provider="google",
            scope=granted_scope,
            access_token=f.encrypt(access_token.encode()),
            refresh_token=f.encrypt(refresh_token.encode()) if refresh_token else b"",
            expiry=expiry
        )
        db.add(tok)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"OAuth token exchange failed for user_id={user.user_id}: {str(e)}")
        raise

def get_gmail_service(access_token: str, refresh_token: str | None, expiry: datetime | None):
    creds = Credentials(token=access_token, refresh_token=refresh_token, token_uri="https://oauth2.googleapis.com/token", client_id=os.getenv("GOOGLE_CLIENT_ID"), client_secret=os.getenv("GOOGLE_CLIENT_SECRET"))
    return build("gmail", "v1", credentials=creds, cache_discovery=False)