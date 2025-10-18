"""
OAuth provider factory.
Returns the appropriate OAuth provider instance based on provider name.
"""

import logging
from typing import Dict, List, Optional
from services.auth.oauth.base import BaseOAuthProvider
from services.auth.oauth.providers.google import GoogleOAuthProvider

logger = logging.getLogger(__name__)


class OAuthProviderFactory:
    """Factory to create OAuth provider instances"""
    
    # Registry of available OAuth providers
    _providers: Dict[str, type] = {
        "google": GoogleOAuthProvider,
        # Future providers will be added here:
        # "yahoo": YahooOAuthProvider,
        # "outlook": OutlookOAuthProvider,
        # "dropbox": DropboxOAuthProvider,
        # "icloud": iCloudOAuthProvider,
    }
    
    @classmethod
    def get_provider(cls, provider_name: str) -> BaseOAuthProvider:
        """
        Get OAuth provider instance by name.
        
        Args:
            provider_name: Provider identifier (e.g., 'google', 'yahoo')
            
        Returns:
            OAuth provider instance
            
        Raises:
            ValueError: If provider is not supported
        """
        provider_name = provider_name.lower().strip()
        provider_class = cls._providers.get(provider_name)
        
        if not provider_class:
            supported = ", ".join(cls._providers.keys())
            raise ValueError(
                f"OAuth provider '{provider_name}' is not supported. "
                f"Supported providers: {supported}"
            )
        
        logger.info(f"Creating OAuth provider instance for: {provider_name}")
        return provider_class()
    
    @classmethod
    def list_providers(cls) -> List[str]:
        """
        List all supported OAuth provider names.
        
        Returns:
            List of provider names
        """
        return list(cls._providers.keys())
    
    @classmethod
    def get_all_provider_info(cls) -> List[Dict]:
        """
        Get information about all supported providers.
        
        Returns:
            List of provider info dictionaries
        """
        providers_info = []
        for provider_name in cls._providers.keys():
            try:
                provider = cls.get_provider(provider_name)
                providers_info.append(provider.get_provider_info())
            except Exception as e:
                logger.error(f"Failed to get info for provider {provider_name}: {str(e)}")
        
        return providers_info
    
    @classmethod
    def is_supported(cls, provider_name: str) -> bool:
        """
        Check if a provider is supported.
        
        Args:
            provider_name: Provider identifier
            
        Returns:
            True if supported, False otherwise
        """
        return provider_name.lower().strip() in cls._providers
    
    @classmethod
    def register_provider(cls, provider_name: str, provider_class: type):
        """
        Register a new OAuth provider (for plugins/extensions).
        
        Args:
            provider_name: Unique provider identifier
            provider_class: Provider class (must inherit from BaseOAuthProvider)
        """
        if not issubclass(provider_class, BaseOAuthProvider):
            raise TypeError("Provider class must inherit from BaseOAuthProvider")
        
        cls._providers[provider_name.lower().strip()] = provider_class
        logger.info(f"Registered new OAuth provider: {provider_name}")
