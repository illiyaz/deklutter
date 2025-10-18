"""
Base connector interface for all storage providers.
All connectors (Gmail, Yahoo, Google Drive, etc.) must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class ProviderType(Enum):
    """Supported provider types"""
    EMAIL_GMAIL = "email_gmail"
    EMAIL_YAHOO = "email_yahoo"
    EMAIL_OUTLOOK = "email_outlook"
    EMAIL_ICLOUD = "email_icloud"
    STORAGE_GDRIVE = "storage_gdrive"
    STORAGE_DROPBOX = "storage_dropbox"
    STORAGE_ONEDRIVE = "storage_onedrive"
    STORAGE_BOX = "storage_box"
    STORAGE_ICLOUD = "storage_icloud"
    PHOTOS_GOOGLE = "photos_google"
    PHOTOS_ICLOUD = "photos_icloud"


class ItemCategory(Enum):
    """Universal item categories"""
    DELETE = "delete"      # Safe to delete (spam, duplicates, etc.)
    REVIEW = "review"      # Needs user review
    KEEP = "keep"          # Important, keep
    ARCHIVE = "archive"    # Archive for later


class BaseConnector(ABC):
    """
    Base class for all storage provider connectors.
    Each provider (Gmail, Drive, etc.) implements this interface.
    """
    
    def __init__(self, provider_type: ProviderType):
        self.provider_type = provider_type
    
    @abstractmethod
    def get_oauth_url(self, user_email: str, state: Optional[str] = None) -> str:
        """
        Generate OAuth authorization URL for the provider.
        
        Args:
            user_email: User's email address
            state: Optional state parameter for OAuth
            
        Returns:
            Authorization URL string
        """
        pass
    
    @abstractmethod
    def exchange_code_for_tokens(self, code: str, user_id: int, db) -> bool:
        """
        Exchange authorization code for access/refresh tokens.
        
        Args:
            code: Authorization code from OAuth callback
            user_id: User ID to associate tokens with
            db: Database session
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def scan_items(
        self, 
        user_id: int, 
        db,
        days_back: int = 30,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Scan user's items (emails, files, photos, etc.).
        
        Args:
            user_id: User ID
            db: Database session
            days_back: Number of days to look back
            limit: Maximum number of items to scan
            filters: Optional filters (e.g., file type, size, etc.)
            
        Returns:
            Dictionary with scan results:
            {
                "summary": {
                    "total_items": int,
                    "counts": {"delete": int, "review": int, "keep": int},
                    "total_size_mb": float
                },
                "items": {
                    "delete": [item_ids],
                    "review": [item_ids],
                    "keep": [item_ids]
                },
                "metadata": {
                    "provider": str,
                    "scan_time": datetime,
                    "filters_applied": dict
                }
            }
        """
        pass
    
    @abstractmethod
    def apply_action(
        self,
        user_id: int,
        db,
        item_ids: List[str],
        action: str = "delete"
    ) -> Dict[str, Any]:
        """
        Apply action to items (delete, archive, label, etc.).
        
        Args:
            user_id: User ID
            db: Database session
            item_ids: List of item IDs to process
            action: Action to perform (delete, archive, label, etc.)
            
        Returns:
            Dictionary with results:
            {
                "success": bool,
                "processed": int,
                "failed": int,
                "action": str,
                "errors": [error_messages]
            }
        """
        pass
    
    @abstractmethod
    def get_item_details(
        self,
        user_id: int,
        db,
        item_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get detailed information about specific items.
        
        Args:
            user_id: User ID
            db: Database session
            item_ids: List of item IDs
            
        Returns:
            List of item details with metadata
        """
        pass
    
    @abstractmethod
    def revoke_access(self, user_id: int, db) -> bool:
        """
        Revoke OAuth access for this provider.
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            True if successful
        """
        pass
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about this provider.
        
        Returns:
            Provider metadata
        """
        return {
            "type": self.provider_type.value,
            "name": self._get_provider_name(),
            "category": self._get_category(),
            "supports": self._get_supported_features()
        }
    
    def _get_provider_name(self) -> str:
        """Get human-readable provider name"""
        names = {
            ProviderType.EMAIL_GMAIL: "Gmail",
            ProviderType.EMAIL_YAHOO: "Yahoo Mail",
            ProviderType.EMAIL_OUTLOOK: "Outlook",
            ProviderType.EMAIL_ICLOUD: "iCloud Mail",
            ProviderType.STORAGE_GDRIVE: "Google Drive",
            ProviderType.STORAGE_DROPBOX: "Dropbox",
            ProviderType.STORAGE_ONEDRIVE: "OneDrive",
            ProviderType.STORAGE_BOX: "Box",
            ProviderType.STORAGE_ICLOUD: "iCloud Drive",
            ProviderType.PHOTOS_GOOGLE: "Google Photos",
            ProviderType.PHOTOS_ICLOUD: "iCloud Photos",
        }
        return names.get(self.provider_type, "Unknown")
    
    def _get_category(self) -> str:
        """Get provider category (email, storage, photos)"""
        if "email" in self.provider_type.value:
            return "email"
        elif "storage" in self.provider_type.value:
            return "storage"
        elif "photos" in self.provider_type.value:
            return "photos"
        return "unknown"
    
    def _get_supported_features(self) -> List[str]:
        """Get list of supported features for this provider"""
        # Override in subclasses
        return ["scan", "delete", "oauth"]
