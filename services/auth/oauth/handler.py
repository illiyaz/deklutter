"""
Unified OAuth handler for all providers and sources (GPT, web, mobile).
"""

import os
import base64
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from cryptography.fernet import Fernet

from services.auth.oauth.factory import OAuthProviderFactory
from services.auth.utils import create_access_token
from db.models import User, OAuthToken

logger = logging.getLogger(__name__)


class UnifiedOAuthHandler:
    """
    Handles OAuth flow for all providers (Google, Yahoo, etc.) 
    and all sources (GPT, webapp, mobile).
    """
    
    def __init__(self, provider_name: str, source: str = "web"):
        """
        Initialize OAuth handler.
        
        Args:
            provider_name: Provider identifier (google, yahoo, dropbox, etc.)
            source: Source of OAuth request (gpt, web, mobile)
        """
        self.provider = OAuthProviderFactory.get_provider(provider_name)
        self.source = source
        self.provider_name = provider_name
    
    def get_auth_url(self, scopes: Optional[List[str]] = None) -> str:
        """
        Generate OAuth authorization URL.
        
        Args:
            scopes: Optional list of OAuth scopes
            
        Returns:
            Authorization URL with state parameter
        """
        # Generate state: provider:source:session_id
        session_id = str(uuid.uuid4())
        state = f"{self.provider_name}:{self.source}:{session_id}"
        
        auth_url = self.provider.get_auth_url(state, scopes)
        
        logger.info(f"Generated OAuth URL for {self.provider_name} (source: {self.source})")
        return auth_url
    
    def handle_callback(
        self, 
        code: str, 
        state: str, 
        db
    ) -> Dict[str, any]:
        """
        Handle OAuth callback from provider.
        
        This method:
        1. Exchanges code for tokens
        2. Gets user info from provider
        3. Creates/updates user in database (auto-signup!)
        4. Stores provider tokens
        5. Generates JWT for your API
        6. Determines redirect URL based on source
        
        Args:
            code: Authorization code from provider
            state: State parameter (provider:source:session_id)
            db: Database session
            
        Returns:
            Dictionary with:
            {
                "user": User object,
                "jwt_token": JWT for your API,
                "redirect_url": Where to redirect user,
                "provider": Provider name,
                "is_new_user": Boolean
            }
        """
        try:
            # Parse state
            parts = state.split(":", 2)
            if len(parts) != 3:
                raise ValueError(f"Invalid state format: {state}")
            
            provider_name, source, session_id = parts
            
            logger.info(f"Processing OAuth callback for {provider_name} (source: {source})")
            
            # Exchange code for tokens
            tokens = self.provider.exchange_code_for_tokens(code)
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token", "")
            expires_in = tokens.get("expires_in", 3600)
            
            if not access_token:
                raise ValueError("No access token received from provider")
            
            # Get user info from provider
            user_info = self.provider.get_user_info(access_token)
            user_email = user_info.get("email")
            
            if not user_email:
                raise ValueError("Could not get user email from provider")
            
            # Get or create user (AUTO-SIGNUP!)
            user = db.query(User).filter(User.email == user_email).first()
            is_new_user = False
            
            if not user:
                # Create new user automatically
                user = User(
                    email=user_email,
                    is_active=True
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                is_new_user = True
                logger.info(f"Created new user: {user_email}")
            else:
                logger.info(f"Existing user: {user_email}")
            
            # Store provider tokens
            self._store_provider_tokens(
                user_id=user.id,
                provider=provider_name,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
                scope=tokens.get("scope", ""),
                db=db
            )
            
            # Generate JWT for your API
            jwt_token = create_access_token({
                "sub": str(user.id),
                "email": user.email
            })
            
            # Determine redirect URL based on source
            redirect_url = self._get_redirect_url(source, jwt_token, session_id)
            
            return {
                "user": user,
                "jwt_token": jwt_token,
                "redirect_url": redirect_url,
                "provider": provider_name,
                "is_new_user": is_new_user
            }
            
        except Exception as e:
            logger.error(f"OAuth callback failed: {str(e)}", exc_info=True)
            raise
    
    def _store_provider_tokens(
        self,
        user_id: int,
        provider: str,
        access_token: str,
        refresh_token: str,
        expires_in: int,
        scope: str,
        db
    ):
        """Store OAuth tokens in database (encrypted)"""
        try:
            # Get encryption key
            f = self._get_fernet()
            
            # Calculate expiry
            expiry = datetime.utcnow() + timedelta(seconds=expires_in)
            
            # Check if token already exists
            existing_token = db.query(OAuthToken).filter(
                OAuthToken.user_id == user_id,
                OAuthToken.provider == provider
            ).first()
            
            if existing_token:
                # Update existing token
                existing_token.access_token = f.encrypt(access_token.encode())
                existing_token.refresh_token = f.encrypt(refresh_token.encode()) if refresh_token else b""
                existing_token.expiry = expiry
                existing_token.scope = scope
                logger.info(f"Updated {provider} tokens for user_id={user_id}")
            else:
                # Create new token
                token = OAuthToken(
                    user_id=user_id,
                    provider=provider,
                    scope=scope,
                    access_token=f.encrypt(access_token.encode()),
                    refresh_token=f.encrypt(refresh_token.encode()) if refresh_token else b"",
                    expiry=expiry
                )
                db.add(token)
                logger.info(f"Stored new {provider} tokens for user_id={user_id}")
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Failed to store provider tokens: {str(e)}")
            raise
    
    def _get_fernet(self) -> Fernet:
        """Get Fernet encryption instance"""
        key = base64.urlsafe_b64encode(
            (os.getenv("APP_SECRET", "change-me") * 2)[:32].encode()
        )
        return Fernet(key)
    
    def _get_redirect_url(self, source: str, jwt_token: str, session_id: str) -> str:
        """
        Get redirect URL based on source.
        
        Args:
            source: Source identifier (gpt, web, mobile)
            jwt_token: JWT token for your API
            session_id: Session identifier
            
        Returns:
            Redirect URL string
        """
        if source == "gpt":
            # For GPT, we need to redirect back to ChatGPT
            # The exact URL format may vary - check OpenAI docs
            # This is a placeholder that should work
            return f"https://chat.openai.com/aip/oauth/callback?token={jwt_token}&state={session_id}"
        
        elif source == "web":
            # For webapp, redirect to dashboard
            webapp_url = os.getenv("WEBAPP_URL", "http://localhost:3000")
            return f"{webapp_url}/dashboard?token={jwt_token}"
        
        elif source == "mobile":
            # For mobile, use deep link
            return f"deklutter://auth/callback?token={jwt_token}&session={session_id}"
        
        else:
            # Default: redirect to API root with token
            api_url = os.getenv("API_URL", "https://deklutter-api.onrender.com")
            return f"{api_url}/?token={jwt_token}"
    
    def revoke_access(self, user_id: int, db) -> bool:
        """
        Revoke OAuth access for a user.
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            True if successful
        """
        try:
            # Get token from database
            token = db.query(OAuthToken).filter(
                OAuthToken.user_id == user_id,
                OAuthToken.provider == self.provider_name
            ).first()
            
            if not token:
                logger.warning(f"No {self.provider_name} token found for user_id={user_id}")
                return False
            
            # Decrypt access token
            f = self._get_fernet()
            access_token = f.decrypt(token.access_token).decode()
            
            # Revoke with provider
            success = self.provider.revoke_token(access_token)
            
            if success:
                # Delete from database
                db.delete(token)
                db.commit()
                logger.info(f"Revoked {self.provider_name} access for user_id={user_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to revoke access: {str(e)}")
            return False
