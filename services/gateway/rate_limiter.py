"""
Rate limiting middleware to prevent abuse
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/hour"],  # Default: 100 requests per hour per IP
    storage_uri="memory://",  # Use in-memory storage (upgrade to Redis for production)
    headers_enabled=True  # Add rate limit headers to responses
)

# Custom rate limit exceeded handler
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded"""
    logger.warning(f"Rate limit exceeded for {get_remote_address(request)}")
    
    return {
        "error": "rate_limit_exceeded",
        "message": "Too many requests. Please slow down.",
        "action": "Wait a few minutes and try again",
        "retry_after": exc.detail
    }

# Rate limit configurations for different endpoints
RATE_LIMITS = {
    # Authentication endpoints - more lenient
    "auth": "20/minute",
    
    # OAuth endpoints - prevent OAuth spam
    "oauth": "10/minute",
    
    # Scan endpoints - expensive operations
    "scan": "5/minute",  # Max 5 scans per minute
    
    # Apply endpoints - destructive operations
    "apply": "10/minute",  # Max 10 cleanup operations per minute
    
    # Health check - very lenient
    "health": "100/minute",
    
    # Default for other endpoints
    "default": "30/minute"
}

def get_rate_limit(endpoint_type: str = "default") -> str:
    """Get rate limit for specific endpoint type"""
    return RATE_LIMITS.get(endpoint_type, RATE_LIMITS["default"])
