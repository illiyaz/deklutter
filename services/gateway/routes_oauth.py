"""
Universal OAuth routes for all providers (Google, Yahoo, Dropbox, etc.)
and all sources (GPT, webapp, mobile).
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session

from services.auth.oauth.handler import UnifiedOAuthHandler
from services.auth.oauth.factory import OAuthProviderFactory
from db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# Request/Response Models
# ============================================================================

class OAuthInitRequest(BaseModel):
    provider: str
    source: str = "web"  # gpt, web, mobile
    scopes: Optional[List[str]] = None


class OAuthInitResponse(BaseModel):
    auth_url: str
    provider: str
    source: str


class ProviderInfo(BaseModel):
    name: str
    display_name: str
    category: str
    default_scopes: List[str]
    supports_refresh: bool


class ProvidersListResponse(BaseModel):
    providers: List[ProviderInfo]


# ============================================================================
# Provider Discovery
# ============================================================================

@router.get("/providers", response_model=ProvidersListResponse)
def list_oauth_providers():
    """
    List all supported OAuth providers.
    
    Returns information about all available providers (Google, Yahoo, etc.)
    """
    try:
        providers_info = OAuthProviderFactory.get_all_provider_info()
        return {"providers": providers_info}
    except Exception as e:
        logger.error(f"Failed to list providers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list providers")


# ============================================================================
# OAuth Initialization
# ============================================================================

@router.post("/{provider}/init", response_model=OAuthInitResponse)
def init_oauth(
    provider: str,
    source: str = Query("web", description="Source: gpt, web, or mobile"),
    scopes: Optional[str] = Query(None, description="Comma-separated scopes")
):
    """
    Initialize OAuth flow for any provider.
    
    **Examples:**
    - `/oauth/google/init?source=gpt` - Gmail for GPT
    - `/oauth/yahoo/init?source=web` - Yahoo for webapp
    - `/oauth/dropbox/init?source=mobile` - Dropbox for mobile
    
    **Parameters:**
    - **provider**: google, yahoo, outlook, dropbox, etc.
    - **source**: gpt (ChatGPT), web (webapp), mobile (mobile app)
    - **scopes**: Optional comma-separated OAuth scopes
    
    **Returns:**
    - **auth_url**: URL for user to authorize
    - **provider**: Provider name
    - **source**: Source identifier
    """
    try:
        # Parse scopes if provided
        scope_list = scopes.split(",") if scopes else None
        
        # Create handler
        handler = UnifiedOAuthHandler(provider, source)
        
        # Generate auth URL
        auth_url = handler.get_auth_url(scope_list)
        
        logger.info(f"OAuth init: provider={provider}, source={source}")
        
        return {
            "auth_url": auth_url,
            "provider": provider,
            "source": source
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"OAuth init failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to initialize OAuth")


# ============================================================================
# OAuth Callback
# ============================================================================

@router.get("/{provider}/callback")
def oauth_callback(
    provider: str,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    error_description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Universal OAuth callback for all providers.
    
    This endpoint:
    1. Receives authorization code from provider
    2. Exchanges code for tokens
    3. Gets user info from provider
    4. Creates/updates user in database (auto-signup!)
    5. Stores provider tokens
    6. Generates JWT for your API
    7. Redirects to appropriate destination (GPT/webapp/mobile)
    
    **Handles:**
    - Google, Yahoo, Outlook, Dropbox, etc.
    - GPT, webapp, mobile sources
    - Auto user creation (zero friction!)
    """
    # Handle errors from provider
    if error:
        error_msg = error_description or error
        logger.error(f"OAuth error from {provider}: {error_msg}")
        
        return HTMLResponse(f"""
        <html>
        <head>
            <title>Authorization Failed</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 40px; text-align: center; }}
                h1 {{ color: #dc2626; }}
                .error {{ background: #fee2e2; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 600px; }}
            </style>
        </head>
        <body>
            <h1>❌ Authorization Failed</h1>
            <div class="error">
                <p><strong>Provider:</strong> {provider}</p>
                <p><strong>Error:</strong> {error_msg}</p>
            </div>
            <p><a href="/">Try again</a></p>
        </body>
        </html>
        """, status_code=400)
    
    # Validate parameters
    if not code or not state:
        logger.error(f"Missing code or state in OAuth callback")
        return HTMLResponse("""
        <html>
        <head>
            <title>Invalid Request</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 40px; text-align: center; }
                h1 { color: #dc2626; }
            </style>
        </head>
        <body>
            <h1>❌ Invalid Request</h1>
            <p>Missing authorization code or state parameter.</p>
            <p><a href="/">Go back</a></p>
        </body>
        </html>
        """, status_code=400)
    
    try:
        # Parse source from state
        parts = state.split(":", 2)
        if len(parts) < 2:
            raise ValueError("Invalid state format")
        
        _, source, _ = parts
        
        # Handle callback
        handler = UnifiedOAuthHandler(provider, source)
        result = handler.handle_callback(code, state, db)
        
        # Log success
        user = result["user"]
        is_new = result["is_new_user"]
        logger.info(
            f"OAuth success: provider={provider}, user={user.email}, "
            f"new_user={is_new}, source={source}"
        )
        
        # For GPT and mobile, redirect with token
        if source in ["gpt", "mobile"]:
            return RedirectResponse(url=result["redirect_url"])
        
        # For web, show success page with token
        jwt_token = result["jwt_token"]
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
                <p>You've successfully connected <strong>{provider.title()}</strong>!</p>
                <p>{"🎉 Welcome! Your account has been created." if is_new else "👋 Welcome back!"}</p>
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
        logger.error(f"OAuth callback error: {str(e)}", exc_info=True)
        
        return HTMLResponse(f"""
        <html>
        <head>
            <title>OAuth Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 40px; text-align: center; }}
                h1 {{ color: #dc2626; }}
                .error {{ background: #fee2e2; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 600px; }}
            </style>
        </head>
        <body>
            <h1>❌ OAuth Error</h1>
            <div class="error">
                <p>An error occurred during authorization.</p>
                <p><small>{str(e)}</small></p>
            </div>
            <p><a href="/">Try again</a></p>
        </body>
        </html>
        """, status_code=500)


# ============================================================================
# OAuth Revocation
# ============================================================================

@router.delete("/{provider}/revoke")
def revoke_oauth(
    provider: str,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Revoke OAuth access for a provider.
    
    **Parameters:**
    - **provider**: google, yahoo, dropbox, etc.
    - **user_id**: User ID to revoke access for
    
    **Note:** In production, user_id should come from JWT token, not query param.
    """
    try:
        handler = UnifiedOAuthHandler(provider, "web")
        success = handler.revoke_access(user_id, db)
        
        if success:
            return {"message": f"Successfully revoked {provider} access"}
        else:
            raise HTTPException(status_code=404, detail=f"No {provider} access found")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Revoke failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to revoke access")
