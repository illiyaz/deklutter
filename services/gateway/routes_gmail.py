import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from services.gateway.deps import get_current_user, CurrentUser
from services.gmail_connector.oauth import get_google_auth_url, exchange_code_store_tokens
from services.gmail_connector.api import scan_recent, apply_cleanup
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
        
        return HTMLResponse("""
        <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1 style="color: green;">✅ Authorization Successful!</h1>
        <p>You can now close this window and run the Gmail scan.</p>
        <p>Go back to your terminal and choose option 3 to scan your Gmail.</p>
        </body></html>
        """)
    except Exception as e:
        logger.error(f"OAuth callback error for user {user_email}: {str(e)}", exc_info=True)
        return HTMLResponse(f"""
        <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1>❌ OAuth Error</h1>
        <p>An error occurred during authorization. Please try again.</p>
        <p style="color: #666; font-size: 14px;">Error: {str(e)}</p>
        </body></html>
        """, status_code=500)

@router.post("/gmail/scan")
def gmail_scan(req: ScanRequest, user: CurrentUser = Depends(get_current_user)):
    plan = scan_recent(user=user, days_back=req.days_back, limit=req.limit)
    return plan

@router.post("/gmail/apply")
def gmail_apply(req: ApplyRequest, user: CurrentUser = Depends(get_current_user)):
    result = apply_cleanup(user=user, message_ids=req.message_ids, mode=req.mode)
    return result