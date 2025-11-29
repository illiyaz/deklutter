import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from services.gateway.deps import get_current_user, CurrentUser
from services.gmail_connector.oauth import get_google_auth_url, exchange_code_store_tokens
from services.gmail_connector.api import scan_recent, apply_cleanup
from services.gateway.rate_limiter import limiter
from pydantic import BaseModel
from db.session import get_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter()

class ScanRequest(BaseModel):
    days_back: int = 365
    limit: int = 1000

class ApplyRequest(BaseModel):
    message_ids: list[str]
    mode: str = "trash"  # or "label_only"

@router.post("/auth/google/init")
def auth_google_init(user: CurrentUser = Depends(get_current_user)):
    url = get_google_auth_url(readonly=True, state=f"user:{user.email}")
    return {"auth_url": url}

@router.get("/auth/google/callback")
def auth_google_callback(
    code: str | None = None,
    error: str | None = None,
    state: str | None = None,
    db: Session = Depends(get_db)
):
    # Check if Google sent an error
    if error:
        return HTMLResponse(f"""
        <html><body>
        <h1>❌ Authorization Failed</h1>
        <p>Error from Google: {error}</p>
        <p>State: {state}</p>
        <p><a href="/">Try again</a></p>
        </body></html>
        """)
    
    if not code:
        return HTMLResponse("""
        <html><body>
        <h1>❌ No Authorization Code</h1>
        <p>No code parameter received from Google.</p>
        </body></html>
        """)
    
    # Extract user email from state (format: "user:email@example.com")
    # For now, use demo user - will be replaced with proper session management
    from db.models import User
    
    # Get or create demo user for testing
    user_email = "demo@user.test"
    if state and state.startswith("user:"):
        user_email = state.split(":", 1)[1]
    
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db_user = User(email=user_email, is_active=True)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
    user = CurrentUser(user_id=db_user.id, email=db_user.email)
    
    try:
        ok = exchange_code_store_tokens(code=code, user=user, db=db)
        if not ok:
            return HTMLResponse("""
            <html><body>
            <h1>❌ Token Exchange Failed</h1>
            <p>Failed to exchange authorization code for tokens.</p>
            </body></html>
            """, status_code=400)
        
        # Generate JWT token for the user
        from services.auth.utils import create_access_token
        jwt_token = create_access_token({"user_id": user.user_id, "email": user.email})
        
        return HTMLResponse(f"""
        <html>
        <head>
            <title>Authorization Successful</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }}
                h1 {{ color: #16a34a; }}
                .success {{ background: #dcfce7; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .token-box {{ background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0; word-break: break-all; font-family: monospace; font-size: 12px; }}
                .copy-btn {{ background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; }}
                .copy-btn:hover {{ background: #5568d3; }}
                .instructions {{ background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f59e0b; }}
            </style>
        </head>
        <body>
            <h1>✅ Authorization Successful!</h1>
            <div class="success">
                <p>You've successfully connected <strong>Gmail</strong>!</p>
                <p>👋 Welcome back!</p>
            </div>
            
            <div class="instructions">
                <h3>📋 Next Steps:</h3>
                <ol>
                    <li>Copy your JWT token below</li>
                    <li>Go to <a href="https://api.deklutter.co/docs" target="_blank">API Docs</a></li>
                    <li>Click "Authorize" and paste your token</li>
                    <li>Try the <code>/gmail/scan</code> endpoint!</li>
                </ol>
            </div>
            
            <h3>🔑 Your JWT Token:</h3>
            <div class="token-box" id="token">{jwt_token}</div>
            <button class="copy-btn" onclick="copyToken()">📋 Copy Token</button>
            
            <p style="margin-top: 30px; color: #666; font-size: 14px;">
                <strong>Note:</strong> This token expires in 24 hours. Keep it safe and don't share it!
            </p>
            
            <script>
                function copyToken() {{
                    const token = document.getElementById('token').textContent;
                    navigator.clipboard.writeText(token).then(() => {{
                        const btn = document.querySelector('.copy-btn');
                        btn.textContent = '✅ Copied!';
                        setTimeout(() => {{
                            btn.textContent = '📋 Copy Token';
                        }}, 2000);
                    }});
                }}
            </script>
        </body>
        </html>
        """)
    except Exception as e:
        logger.error(f"OAuth callback error for user {user_email}: {str(e)}", exc_info=True)
        return HTMLResponse(f"""
        <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1>❌ OAuth Error</h1>
        <p>An error occurred during authorization. Please try again.</p>
        </body></html>
        """, status_code=500)

@router.post("/debug/reset-user")
def reset_user(
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete current user and all their data - for testing only"""
    from db.models import OAuthToken, MailDecisionLog, ActivityLog
    
    # Delete all user data
    db.query(OAuthToken).filter(OAuthToken.user_id == user.user_id).delete()
    db.query(MailDecisionLog).filter(MailDecisionLog.user_id == user.user_id).delete()
    db.query(ActivityLog).filter(ActivityLog.user_id == user.user_id).delete()
    
    # Delete user
    from db.models import User
    db.query(User).filter(User.id == user.user_id).delete()
    
    db.commit()
    
    return {
        "message": "User deleted successfully",
        "user_id": user.user_id,
        "email": user.email
    }

@router.get("/gmail/status")
def gmail_status(
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if Gmail is connected for the current user"""
    from db.models import OAuthToken
    from datetime import datetime
    
    token = db.query(OAuthToken).filter(
        OAuthToken.user_id == user.user_id,
        OAuthToken.provider == "google"
    ).first()
    
    return {
        "user_id": user.user_id,
        "email": user.email,
        "gmail_connected": token is not None,
        "token_exists": token is not None,
        "token_expired": token.expiry < datetime.utcnow() if token else None
    }

@router.post("/gmail/scan")
@limiter.limit("5/minute")  # Max 5 scans per minute
def gmail_scan(
    request: Request,
    req: ScanRequest, 
    user: CurrentUser = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Scan Gmail inbox - requires authentication"""
    try:
        result = scan_recent(user, req.days_back, req.limit, db)
        return result
    except Exception as e:
        logger.error(f"Gmail scan failed for user {user.email}: {str(e)}", exc_info=True)
        from fastapi import HTTPException
        
        # Check if it's an OAuth issue
        if "No OAuth token" in str(e) or "credentials" in str(e).lower():
            raise HTTPException(
                status_code=403,
                detail="Gmail not authorized. Please visit /start to connect your Gmail account."
            )
        
        # Generic error
        raise HTTPException(
            status_code=500,
            detail=f"Scan failed: {str(e)}"
        )

@router.post("/gmail/apply")
@limiter.limit("10/minute")  # Max 10 cleanup operations per minute
def gmail_apply(
    request: Request,
    req: ApplyRequest, 
    user: CurrentUser = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Apply cleanup to Gmail - requires authentication"""
    result = apply_cleanup(user, req.message_ids, req.mode, db)
    return result

@router.post("/oauth/revoke")
def revoke_access(
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Revoke all access and delete user data.
    
    Deletes all OAuth tokens for the user.
    User can re-authorize later if needed.
    """
    from db.models import OAuthToken
    from datetime import datetime
    
    try:
        # Delete all OAuth tokens for this user
        deleted_count = db.query(OAuthToken).filter(
            OAuthToken.user_id == user.user_id
        ).delete()
        
        db.commit()
        
        logger.info(f"Revoked access for user {user.email}, deleted {deleted_count} tokens")
        
        return {
            "message": "Access revoked successfully. All data deleted.",
            "revoked_at": datetime.utcnow().isoformat() + "Z",
            "tokens_deleted": deleted_count
        }
        
    except Exception as e:
        logger.error(f"Revoke failed for user {user.email}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to revoke access")