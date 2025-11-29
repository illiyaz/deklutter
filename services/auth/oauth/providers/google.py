"""
Google OAuth provider implementation.
"""

import os
import logging
from typing import Dict, List, Optional
from google_auth_oauthlib.flow import Flow
import requests

from services.auth.oauth.base import BaseOAuthProvider

logger = logging.getLogger(__name__)


class GoogleOAuthProvider(BaseOAuthProvider):
    """Google OAuth 2.0 implementation"""
    
    def __init__(self):
        super().__init__("google")
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            logger.warning("Google OAuth credentials not fully configured")
    
    def get_auth_url(self, state: str, scopes: Optional[List[str]] = None) -> str:
        """Generate Google OAuth authorization URL"""
        scopes = scopes or self.get_default_scopes()
        
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
            scopes=scopes
        )
        flow.redirect_uri = self.redirect_uri
        
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
            state=state
        )
        
        logger.info(f"Generated Google OAuth URL with state: {state}")
        return auth_url
    
    def exchange_code_for_tokens(self, code: str) -> Dict[str, str]:
        """Exchange authorization code for Google tokens"""
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
            
            logger.info("Successfully exchanged code for Google tokens")
            
            return {
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token", ""),
                "expires_in": token_data.get("expires_in", 3600),
                "scope": token_data.get("scope", " ".join(self.get_default_scopes()))
            }
            
        except Exception as e:
            logger.error(f"Failed to exchange code for Google tokens: {str(e)}")
            raise
    
    def get_user_info(self, access_token: str) -> Dict[str, str]:
        """Get user information from Google"""
        try:
            response = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            data = response.json()
            
            user_info = {
                "email": data.get("email"),
                "name": data.get("name", ""),
                "picture": data.get("picture", ""),
                "id": data.get("id", "")
            }
            
            logger.info(f"Retrieved user info for: {user_info['email']}")
            return user_info
            
        except Exception as e:
            logger.error(f"Failed to get Google user info: {str(e)}")
            raise
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, str]:
        """Refresh Google access token"""
        try:
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "refresh_token": refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token"
            }
            
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            logger.info("Successfully refreshed Google access token")
            
            return {
                "access_token": token_data.get("access_token"),
                "expires_in": token_data.get("expires_in", 3600),
                "scope": token_data.get("scope", "")
            }
            
        except Exception as e:
            logger.error(f"Failed to refresh Google token: {str(e)}")
            raise
    
    def revoke_token(self, token: str) -> bool:
        """Revoke Google access token"""
        try:
            response = requests.post(
                f"https://oauth2.googleapis.com/revoke?token={token}"
            )
            success = response.status_code == 200
            
            if success:
                logger.info("Successfully revoked Google token")
            else:
                logger.warning(f"Failed to revoke Google token: {response.status_code}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error revoking Google token: {str(e)}")
            return False
    
    def get_default_scopes(self) -> List[str]:
        """Get default Google OAuth scopes - minimal permissions"""
        return [
            "https://www.googleapis.com/auth/gmail.readonly",   # Read emails for scanning
            "https://www.googleapis.com/auth/gmail.modify",     # Trash/label emails
            "https://www.googleapis.com/auth/userinfo.email"    # Get user email (for account identification)
            # Note: userinfo.profile removed - we don't need name/photo
        ]
    
    def _get_category(self) -> str:
        """Google is primarily an email provider"""
        return "email"
