"""
Universal routes for all providers (Gmail, Yahoo, Drive, Dropbox, etc.)
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session

from services.gateway.deps import get_current_user, CurrentUser
from services.connectors.factory import ConnectorFactory
from services.connectors.base import ProviderType
from db.session import get_db
from db.models import User

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# Request/Response Models
# ============================================================================

class ScanRequest(BaseModel):
    provider: str = "gmail"  # gmail, yahoo, gdrive, dropbox, etc.
    days_back: int = 30
    limit: int = 100
    filters: Optional[dict] = None


class ApplyRequest(BaseModel):
    provider: str = "gmail"
    item_ids: List[str]
    action: str = "delete"  # delete, trash, archive, label


class ProviderListResponse(BaseModel):
    providers: List[dict]


# ============================================================================
# Provider Discovery
# ============================================================================

@router.get("/providers", response_model=ProviderListResponse)
def list_providers():
    """
    List all supported providers.
    
    Returns information about supported email providers, cloud storage, etc.
    """
    providers = ConnectorFactory.list_supported_providers()
    return {"providers": providers}


# ============================================================================
# OAuth Flow
# ============================================================================

@router.post("/connect/{provider}")
def connect_provider(
    provider: str,
    user: CurrentUser = Depends(get_current_user)
):
    """
    Initialize OAuth flow for a provider.
    
    Supported providers: gmail, yahoo, outlook, gdrive, dropbox, etc.
    """
    try:
        connector = ConnectorFactory.get_connector_by_name(provider)
        auth_url = connector.get_oauth_url(user.email, state=f"user:{user.email}")
        
        return {
            "provider": provider,
            "auth_url": auth_url,
            "message": f"Please visit the URL to authorize {connector.get_provider_info()['name']}"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to initialize OAuth for {provider}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to initialize authorization")


@router.get("/callback/{provider}")
def oauth_callback(
    provider: str,
    code: Optional[str] = None,
    error: Optional[str] = None,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    OAuth callback endpoint for all providers.
    
    This is called by the provider after user authorizes access.
    """
    # Check for errors
    if error:
        return HTMLResponse(f"""
        <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1>❌ Authorization Failed</h1>
        <p>Error from {provider}: {error}</p>
        <p><a href="/">Try again</a></p>
        </body></html>
        """)
    
    if not code:
        return HTMLResponse("""
        <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1>❌ No Authorization Code</h1>
        <p>No code parameter received.</p>
        </body></html>
        """)
    
    # Extract user email from state
    user_email = "demo@user.test"
    if state and state.startswith("user:"):
        user_email = state.split(":", 1)[1]
    
    # Get or create user
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db_user = User(email=user_email, is_active=True)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
    try:
        # Exchange code for tokens
        connector = ConnectorFactory.get_connector_by_name(provider)
        success = connector.exchange_code_for_tokens(code, db_user.id, db)
        
        if not success:
            return HTMLResponse("""
            <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
            <h1>❌ Token Exchange Failed</h1>
            <p>Failed to exchange authorization code for tokens.</p>
            </body></html>
            """, status_code=400)
        
        provider_name = connector.get_provider_info()['name']
        # Generate JWT token
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
                <p>You've successfully connected <strong>{provider_name}</strong>!</p>
            </div>
            
            <div class="instructions">
                <h3>📋 Next Steps:</h3>
                <ol>
                    <li>Copy your JWT token below</li>
                    <li>Go to <a href="https://api.deklutter.co/docs" target="_blank">API Docs</a></li>
                    <li>Click "Authorize" and paste your token</li>
                    <li>Try scanning your inbox!</li>
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
        logger.error(f"OAuth callback error for {provider}: {str(e)}", exc_info=True)
        return HTMLResponse(f"""
        <html><body style="font-family: sans-serif; padding: 40px; text-align: center;">
        <h1>❌ OAuth Error</h1>
        <p>An error occurred during authorization. Please try again.</p>
        <p style="color: #666; font-size: 14px;">Error: {str(e)}</p>
        </body></html>
        """, status_code=500)


# ============================================================================
# Scanning
# ============================================================================

@router.post("/scan")
def scan_items(
    req: ScanRequest,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Scan items from any provider.
    
    Supports: Gmail, Yahoo, Outlook, Google Drive, Dropbox, etc.
    """
    try:
        connector = ConnectorFactory.get_connector_by_name(req.provider)
        result = connector.scan_items(
            user_id=user.user_id,
            db=db,
            days_back=req.days_back,
            limit=req.limit,
            filters=req.filters
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Scan failed for {req.provider}: {str(e)}")
        raise HTTPException(status_code=500, detail="Scan failed")


# ============================================================================
# Apply Actions
# ============================================================================

@router.post("/apply")
def apply_action(
    req: ApplyRequest,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Apply action to items (delete, archive, etc.).
    
    Supports all connected providers.
    """
    try:
        connector = ConnectorFactory.get_connector_by_name(req.provider)
        result = connector.apply_action(
            user_id=user.user_id,
            db=db,
            item_ids=req.item_ids,
            action=req.action
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Apply action failed for {req.provider}: {str(e)}")
        raise HTTPException(status_code=500, detail="Action failed")


# ============================================================================
# Item Details
# ============================================================================

@router.get("/items/{provider}")
def get_item_details(
    provider: str,
    item_ids: str = Query(..., description="Comma-separated item IDs"),
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about specific items.
    """
    try:
        connector = ConnectorFactory.get_connector_by_name(provider)
        ids = item_ids.split(",")
        details = connector.get_item_details(
            user_id=user.user_id,
            db=db,
            item_ids=ids
        )
        
        return {"items": details}
        
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Get details failed for {provider}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get details")


# ============================================================================
# Disconnect
# ============================================================================

@router.delete("/disconnect/{provider}")
def disconnect_provider(
    provider: str,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Disconnect and revoke access for a provider.
    """
    try:
        connector = ConnectorFactory.get_connector_by_name(provider)
        success = connector.revoke_access(user_id=user.user_id, db=db)
        
        if success:
            return {"message": f"Successfully disconnected {provider}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to disconnect")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Disconnect failed for {provider}: {str(e)}")
        raise HTTPException(status_code=500, detail="Disconnect failed")
