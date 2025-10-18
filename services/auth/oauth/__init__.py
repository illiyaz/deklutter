"""
Universal OAuth system for all providers.
"""

from services.auth.oauth.base import BaseOAuthProvider
from services.auth.oauth.factory import OAuthProviderFactory
from services.auth.oauth.handler import UnifiedOAuthHandler

__all__ = ["BaseOAuthProvider", "OAuthProviderFactory", "UnifiedOAuthHandler"]
