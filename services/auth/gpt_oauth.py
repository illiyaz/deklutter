"""
OAuth endpoints specifically for GPT Actions.
Provides secure authentication for ChatGPT to access user's Gmail.
"""

import os
import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session

from db.session import get_db
from db.models import User, OAuthToken, OAuthState
from services.auth.oauth.handler import UnifiedOAuthHandler
from services.auth.utils import create_access_token, create_refresh_token

logger = logging.getLogger(__name__)

router = APIRouter()


# Helper functions for database-backed OAuth state management
def create_oauth_state(db: Session, state: str, provider: str, source: str, 
                       gpt_state: str = None, gpt_redirect_uri: str = None,
                       client_id: str = None) -> OAuthState:
    """Create a new OAuth state in database"""
    expires_at = datetime.utcnow() + timedelta(minutes=30)  # 30 min expiry
    
    oauth_state = OAuthState(
        state=state,
        provider=provider,
        source=source,
        redirect_uri=gpt_redirect_uri,
        expires_at=expires_at
    )
    
    db.add(oauth_state)
    db.commit()
    db.refresh(oauth_state)
    
    logger.info(f"Created OAuth state: {state} (expires in 30 min)")
    return oauth_state


def get_oauth_state(db: Session, state: str) -> Optional[OAuthState]:
    """Get OAuth state from database"""
    oauth_state = db.query(OAuthState).filter(
        OAuthState.state == state,
        OAuthState.expires_at > datetime.utcnow()  # Not expired
    ).first()
    
    return oauth_state


def delete_oauth_state(db: Session, state: str):
    """Delete OAuth state from database"""
    db.query(OAuthState).filter(OAuthState.state == state).delete()
    db.commit()
    logger.info(f"Deleted OAuth state: {state}")


def cleanup_expired_states(db: Session):
    """Clean up expired OAuth states (called periodically)"""
    deleted = db.query(OAuthState).filter(
        OAuthState.expires_at <= datetime.utcnow()
    ).delete()
    
    if deleted > 0:
        db.commit()
        logger.info(f"Cleaned up {deleted} expired OAuth states")
    
    return deleted


# In-memory storage for refresh tokens (TODO: move to Redis in production)
_refresh_tokens = {}


@router.get("/gpt/oauth/authorize")
def gpt_oauth_authorize(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str = "",
    state: str = "",
    db: Session = Depends(get_db)
):
    """
    GPT OAuth authorization endpoint.
    
    This is called by ChatGPT when user needs to authorize.
    We redirect to Google OAuth, then back to GPT.
    """
    try:
        # Clean up expired states first
        cleanup_expired_states(db)
        
        # Generate unique session ID
        oauth_session_id = secrets.token_urlsafe(32)
        
        # Store GPT's state and redirect_uri in DATABASE
        # We'll store the full state string with gpt_state embedded
        full_state = f"google:gpt:{oauth_session_id}:gptstate:{state}"
        
        create_oauth_state(
            db=db,
            state=full_state,
            provider="google",
            source="gpt",
            gpt_state=state,
            gpt_redirect_uri=redirect_uri,
            client_id=client_id
        )
        
        # Start Google OAuth flow with GPT-specific redirect URI
        handler = UnifiedOAuthHandler("google", "gpt")
        
        # Override redirect URI for GPT flow
        base_url = os.getenv("API_URL", "https://deklutter-api.onrender.com")
        gpt_callback_uri = f"{base_url}/auth/gpt/oauth/callback"
        handler.provider.redirect_uri = gpt_callback_uri
        
        # Get auth URL - it will have state like "google:gpt:uuid"
        google_auth_url = handler.get_auth_url()
        
        # Replace the handler's UUID with our full state
        # Extract and decode the original state from URL
        import re
        from urllib.parse import unquote, quote
        
        state_match = re.search(r'state=([^&]+)', google_auth_url)
        if state_match:
            encoded_original_state = state_match.group(1)
            original_state = unquote(encoded_original_state)
            
            # Replace with our full state (includes gpt_state)
            encoded_new_state = quote(full_state, safe='')
            
            google_auth_url = google_auth_url.replace(
                f"state={encoded_original_state}", 
                f"state={encoded_new_state}"
            )
            
            logger.info(f"GPT OAuth: created state in DB (session: {oauth_session_id})")
        
        logger.info(f"GPT OAuth authorize: redirecting to Google")
        
        # Redirect user to Google OAuth
        return RedirectResponse(url=google_auth_url)
        
    except Exception as e:
        logger.error(f"GPT OAuth authorize failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Authorization failed")


@router.get("/gpt/oauth/callback")
def gpt_oauth_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Callback from Google OAuth.
    
    After user authorizes Google, we:
    1. Exchange code for Google tokens
    2. Create/update user
    3. Generate our own access token
    4. Redirect back to GPT with our token
    """
    if error:
        logger.error(f"Google OAuth error: {error}")
        return HTMLResponse(f"""
        <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1>❌ Authorization Failed</h1>
        <p>Error: {error}</p>
        <p>Please try again.</p>
        </body></html>
        """, status_code=400)
    
    if not code or not state:
        return HTMLResponse("""
        <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1>❌ Invalid Request</h1>
        <p>Missing authorization code or state.</p>
        </body></html>
        """, status_code=400)
    
    try:
        # Parse state - format: google:gpt:session_id:gptstate:original_gpt_state
        logger.info(f"GPT OAuth callback received with state: {state}")
        
        # Retrieve OAuth state from DATABASE
        oauth_state_record = get_oauth_state(db, state)
        
        if not oauth_state_record:
            logger.error(f"OAuth state not found or expired: {state}")
            raise ValueError("OAuth session not found or expired")
        
        # Extract GPT's original state and redirect URI from database
        gpt_redirect_uri = oauth_state_record.redirect_uri
        
        # Extract gpt_state from the state string
        parts = state.split(":gptstate:")
        gpt_state = parts[1] if len(parts) > 1 else ""
        
        logger.info(f"Found OAuth state in DB, redirecting to: {gpt_redirect_uri}")
        
        # Clean up state from database
        delete_oauth_state(db, state)
        
        # Handle Google OAuth callback with GPT-specific redirect URI
        handler = UnifiedOAuthHandler("google", "gpt")
        
        # Override redirect URI for token exchange
        base_url = os.getenv("API_URL", "https://deklutter-api.onrender.com")
        gpt_callback_uri = f"{base_url}/auth/gpt/oauth/callback"
        handler.provider.redirect_uri = gpt_callback_uri
        
        result = handler.handle_callback(code, state, db)
        
        user = result["user"]
        
        # Generate tokens for GPT to use
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "provider": "google"
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        # Store refresh token in memory for later use
        # TODO: Move to Redis in production
        _refresh_tokens[f"refresh_{user.id}"] = refresh_token
        
        logger.info(f"GPT OAuth success for user: {user.email}")
        
        # Redirect back to GPT with our access token
        # GPT will exchange this for the full token response
        redirect_url = f"{gpt_redirect_uri}?code={access_token}&state={gpt_state}"
        
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        logger.error(f"GPT OAuth callback failed: {str(e)}", exc_info=True)
        return HTMLResponse(f"""
        <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1>❌ OAuth Error</h1>
        <p>An error occurred during authorization.</p>
        <p><small>{str(e)}</small></p>
        </body></html>
        """, status_code=500)


@router.post("/gpt/oauth/token")
def gpt_oauth_token(
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...)
):
    """
    GPT OAuth token exchange endpoint.
    
    GPT calls this to exchange the authorization code for an access token.
    In our case, the 'code' is already our access token (from callback).
    """
    try:
        if grant_type != "authorization_code":
            raise HTTPException(status_code=400, detail="Invalid grant_type")
        
        # Validate client credentials
        expected_client_id = os.getenv("GPT_CLIENT_ID", "deklutter-gpt")
        expected_client_secret = os.getenv("GPT_CLIENT_SECRET", "change-me-in-production")
        
        if client_id != expected_client_id or client_secret != expected_client_secret:
            raise HTTPException(status_code=401, detail="Invalid client credentials")
        
        # In our flow, the 'code' is already the access token
        # (we returned it in the callback redirect)
        access_token = code
        
        # Decode to get user info
        from services.auth.utils import decode_access_token
        payload = decode_access_token(access_token)
        user_id = payload.get("sub")
        
        # Get refresh token from storage
        refresh_token = _refresh_tokens.get(f"refresh_{user_id}", "")
        
        logger.info("GPT OAuth token exchange successful")
        
        # Return tokens in OAuth format
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 3600  # 1 hour
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"GPT OAuth token exchange failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Token exchange failed")


@router.post("/gpt/oauth/refresh")
def gpt_oauth_refresh(
    grant_type: str = Form(...),
    refresh_token: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...)
):
    """
    Refresh access token using refresh token.
    
    GPT calls this automatically when access token expires.
    """
    try:
        if grant_type != "refresh_token":
            raise HTTPException(status_code=400, detail="Invalid grant_type")
        
        # Validate client credentials
        expected_client_id = os.getenv("GPT_CLIENT_ID", "deklutter-gpt")
        expected_client_secret = os.getenv("GPT_CLIENT_SECRET", "change-me-in-production")
        
        if client_id != expected_client_id or client_secret != expected_client_secret:
            raise HTTPException(status_code=401, detail="Invalid client credentials")
        
        # Decode and validate refresh token
        from services.auth.utils import decode_refresh_token
        payload = decode_refresh_token(refresh_token)
        
        # Generate new access token
        token_data = {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "provider": payload.get("provider", "google")
        }
        
        new_access_token = create_access_token(token_data)
        
        logger.info(f"Token refreshed for user: {payload.get('email')}")
        
        # Return new access token (refresh token stays the same)
        return {
            "access_token": new_access_token,
            "token_type": "Bearer",
            "expires_in": 3600  # 1 hour
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.post("/gpt/oauth/revoke")
def gpt_oauth_revoke(
    token: str = Form(...),
    token_type_hint: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Revoke access token and delete all user data.
    
    User can call this to completely remove Deklutter's access to their Gmail.
    """
    try:
        # Decode token to get user info
        from services.auth.utils import decode_access_token
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        user_email = payload.get("email")
        
        # Delete all OAuth tokens for this user
        db.query(OAuthToken).filter(OAuthToken.user_id == user_id).delete()
        
        # Clean up refresh token from memory
        if f"refresh_{user_id}" in _refresh_tokens:
            del _refresh_tokens[f"refresh_{user_id}"]
        
        db.commit()
        
        logger.info(f"Revoked all access for user: {user_email}")
        
        return {"message": "Access revoked successfully"}
        
    except Exception as e:
        logger.error(f"Revoke failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Revoke failed")


@router.post("/gpt/oauth/cleanup")
def cleanup_oauth_states_endpoint(db: Session = Depends(get_db)):
    """
    Cleanup expired OAuth states.
    
    Can be called manually or by a cron job.
    """
    try:
        deleted = cleanup_expired_states(db)
        return {
            "message": f"Cleaned up {deleted} expired OAuth states",
            "deleted_count": deleted
        }
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Cleanup failed")
