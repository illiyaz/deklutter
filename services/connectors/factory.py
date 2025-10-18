"""
Connector factory to get the appropriate connector for each provider.
"""

from typing import Optional
from services.connectors.base import BaseConnector, ProviderType
from services.connectors.gmail.connector import GmailConnector


class ConnectorFactory:
    """Factory to create connector instances"""
    
    _connectors = {
        ProviderType.EMAIL_GMAIL: GmailConnector,
        # Future connectors will be added here:
        # ProviderType.EMAIL_YAHOO: YahooConnector,
        # ProviderType.EMAIL_OUTLOOK: OutlookConnector,
        # ProviderType.STORAGE_GDRIVE: GDriveConnector,
        # ProviderType.STORAGE_DROPBOX: DropboxConnector,
    }
    
    @classmethod
    def get_connector(cls, provider_type: ProviderType) -> BaseConnector:
        """
        Get connector instance for the specified provider.
        
        Args:
            provider_type: Type of provider
            
        Returns:
            Connector instance
            
        Raises:
            ValueError: If provider is not supported
        """
        connector_class = cls._connectors.get(provider_type)
        if not connector_class:
            raise ValueError(f"Provider {provider_type.value} is not yet supported")
        
        return connector_class()
    
    @classmethod
    def get_connector_by_name(cls, provider_name: str) -> BaseConnector:
        """
        Get connector by provider name string.
        
        Args:
            provider_name: Provider name (e.g., "gmail", "yahoo", "gdrive")
            
        Returns:
            Connector instance
        """
        # Map common names to ProviderType
        name_mapping = {
            "gmail": ProviderType.EMAIL_GMAIL,
            "google_mail": ProviderType.EMAIL_GMAIL,
            "yahoo": ProviderType.EMAIL_YAHOO,
            "yahoo_mail": ProviderType.EMAIL_YAHOO,
            "outlook": ProviderType.EMAIL_OUTLOOK,
            "microsoft": ProviderType.EMAIL_OUTLOOK,
            "icloud": ProviderType.EMAIL_ICLOUD,
            "icloud_mail": ProviderType.EMAIL_ICLOUD,
            "gdrive": ProviderType.STORAGE_GDRIVE,
            "google_drive": ProviderType.STORAGE_GDRIVE,
            "dropbox": ProviderType.STORAGE_DROPBOX,
            "onedrive": ProviderType.STORAGE_ONEDRIVE,
            "box": ProviderType.STORAGE_BOX,
            "icloud_drive": ProviderType.STORAGE_ICLOUD,
            "google_photos": ProviderType.PHOTOS_GOOGLE,
            "icloud_photos": ProviderType.PHOTOS_ICLOUD,
        }
        
        provider_type = name_mapping.get(provider_name.lower())
        if not provider_type:
            raise ValueError(f"Unknown provider name: {provider_name}")
        
        return cls.get_connector(provider_type)
    
    @classmethod
    def list_supported_providers(cls) -> list[dict]:
        """
        List all supported providers with their info.
        
        Returns:
            List of provider information dictionaries
        """
        providers = []
        for provider_type, connector_class in cls._connectors.items():
            connector = connector_class()
            providers.append(connector.get_provider_info())
        
        return providers
    
    @classmethod
    def is_supported(cls, provider_type: ProviderType) -> bool:
        """Check if a provider is supported"""
        return provider_type in cls._connectors
