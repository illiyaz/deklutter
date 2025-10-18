"""
Base OAuth provider interface.
All OAuth providers (Google, Yahoo, Dropbox, etc.) must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime


class BaseOAuthProvider(ABC):
    """Base class for all OAuth providers"""
    
    def __init__(self, provider_name: str):
        """
        Initialize OAuth provider.
        
        Args:
            provider_name: Unique identifier for provider (e.g., 'google', 'yahoo')
        """
        self.provider_name = provider_name
    
    @abstractmethod
    def get_auth_url(self, state: str, scopes: Optional[List[str]] = None) -> str:
        """
        Generate OAuth authorization URL.
        
        Args:
            state: State parameter for OAuth flow (contains provider:source:session_id)
            scopes: Optional list of OAuth scopes to request
            
        Returns:
            Authorization URL string
        """
        pass
    
    @abstractmethod
    def exchange_code_for_tokens(self, code: str) -> Dict[str, str]:
        """
        Exchange authorization code for access/refresh tokens.
        
        Args:
            code: Authorization code from OAuth callback
            
        Returns:
            Dictionary with tokens:
            {
                "access_token": str,
                "refresh_token": str (optional),
                "expires_in": int (optional),
                "scope": str (optional)
            }
        """
        pass
    
    @abstractmethod
    def get_user_info(self, access_token: str) -> Dict[str, str]:
        """
        Get user information from provider using access token.
        
        Args:
            access_token: OAuth access token
            
        Returns:
            Dictionary with user info:
            {
                "email": str (required),
                "name": str (optional),
                "picture": str (optional),
                "id": str (optional)
            }
        """
        pass
    
    @abstractmethod
    def refresh_access_token(self, refresh_token: str) -> Dict[str, str]:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: OAuth refresh token
            
        Returns:
            Dictionary with new tokens (same format as exchange_code_for_tokens)
        """
        pass
    
    @abstractmethod
    def revoke_token(self, token: str) -> bool:
        """
        Revoke access token.
        
        Args:
            token: Access token to revoke
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_default_scopes(self) -> List[str]:
        """
        Get default OAuth scopes for this provider.
        
        Returns:
            List of scope strings
        """
        pass
    
    def get_provider_info(self) -> Dict[str, any]:
        """
        Get provider metadata.
        
        Returns:
            Dictionary with provider information
        """
        return {
            "name": self.provider_name,
            "display_name": self._get_display_name(),
            "category": self._get_category(),
            "default_scopes": self.get_default_scopes(),
            "supports_refresh": self._supports_refresh_token()
        }
    
    def _get_display_name(self) -> str:
        """Get human-readable provider name"""
        names = {
            "google": "Google",
            "yahoo": "Yahoo",
            "outlook": "Microsoft Outlook",
            "dropbox": "Dropbox",
            "icloud": "iCloud",
        }
        return names.get(self.provider_name, self.provider_name.title())
    
    def _get_category(self) -> str:
        """Get provider category (email, storage, photos)"""
        # Override in subclasses if needed
        return "general"
    
    def _supports_refresh_token(self) -> bool:
        """Check if provider supports refresh tokens"""
        # Override in subclasses if needed
        return True
