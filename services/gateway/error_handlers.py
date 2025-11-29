"""
Centralized error handling for better user experience
"""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)

# User-friendly error messages
ERROR_MESSAGES = {
    # Authentication errors
    "not_authenticated": {
        "message": "You need to sign in first. Please visit /start to connect your Gmail account.",
        "action": "Visit https://api.deklutter.co/start to authorize"
    },
    "token_expired": {
        "message": "Your session has expired. Please sign in again.",
        "action": "Visit https://api.deklutter.co/start to re-authorize"
    },
    "invalid_token": {
        "message": "Invalid authentication token. Please sign in again.",
        "action": "Visit https://api.deklutter.co/start to get a new token"
    },
    
    # OAuth errors
    "oauth_failed": {
        "message": "Failed to connect to Gmail. Please try again.",
        "action": "Visit https://api.deklutter.co/start to retry"
    },
    "no_refresh_token": {
        "message": "Your Gmail connection needs to be refreshed. Please reconnect.",
        "action": "Visit https://api.deklutter.co/start to reconnect"
    },
    
    # Gmail API errors
    "gmail_not_authorized": {
        "message": "Gmail is not connected. Please authorize access first.",
        "action": "Visit https://api.deklutter.co/start to connect Gmail"
    },
    "gmail_quota_exceeded": {
        "message": "Gmail API quota exceeded. Please try again in a few minutes.",
        "action": "Wait 5-10 minutes and try again"
    },
    "gmail_rate_limit": {
        "message": "Too many requests. Please slow down.",
        "action": "Wait 1 minute and try again"
    },
    
    # Scan errors
    "scan_failed": {
        "message": "Failed to scan your inbox. Please try again.",
        "action": "Try scanning fewer emails or a shorter time period"
    },
    "no_emails_found": {
        "message": "No emails found in the specified time period.",
        "action": "Try increasing the days_back parameter"
    },
    
    # Apply errors
    "apply_failed": {
        "message": "Failed to clean up emails. Please try again.",
        "action": "Check if the email IDs are valid and try again"
    },
    "invalid_message_ids": {
        "message": "Some email IDs are invalid or no longer exist.",
        "action": "Scan your inbox again to get fresh email IDs"
    },
    
    # Database errors
    "database_error": {
        "message": "Database error. Our team has been notified.",
        "action": "Please try again in a few minutes"
    },
    
    # Generic errors
    "internal_error": {
        "message": "Something went wrong. Our team has been notified.",
        "action": "Please try again or contact support"
    }
}

def get_user_friendly_error(error_code: str, details: str = None) -> dict:
    """Get user-friendly error message"""
    error_info = ERROR_MESSAGES.get(error_code, ERROR_MESSAGES["internal_error"])
    
    response = {
        "error": error_code,
        "message": error_info["message"],
        "action": error_info["action"]
    }
    
    if details:
        response["details"] = details
    
    return response

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with user-friendly messages"""
    errors = exc.errors()
    
    # Extract field names and error messages
    field_errors = []
    for error in errors:
        field = " -> ".join(str(loc) for loc in error["loc"])
        field_errors.append(f"{field}: {error['msg']}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "message": "Invalid request data. Please check your input.",
            "details": field_errors,
            "action": "Check the API documentation at https://api.deklutter.co/docs"
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with user-friendly messages"""
    
    # Map status codes to error codes
    error_code_map = {
        401: "not_authenticated",
        403: "gmail_not_authorized",
        404: "not_found",
        429: "gmail_rate_limit",
        500: "internal_error"
    }
    
    error_code = error_code_map.get(exc.status_code, "internal_error")
    
    # If detail contains specific error info, try to extract it
    detail = str(exc.detail)
    if "not authorized" in detail.lower() or "no oauth token" in detail.lower():
        error_code = "gmail_not_authorized"
    elif "expired" in detail.lower():
        error_code = "token_expired"
    elif "quota" in detail.lower():
        error_code = "gmail_quota_exceeded"
    
    return JSONResponse(
        status_code=exc.status_code,
        content=get_user_friendly_error(error_code, detail if detail != error_code else None),
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    logger.error(f"Database error: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=get_user_friendly_error("database_error", "Database operation failed"),
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

async def gmail_api_exception_handler(request: Request, exc: HttpError):
    """Handle Gmail API errors"""
    logger.error(f"Gmail API error: {str(exc)}", exc_info=True)
    
    # Parse Gmail API error
    error_code = "gmail_api_error"
    status_code = exc.resp.status
    
    if status_code == 401:
        error_code = "gmail_not_authorized"
    elif status_code == 403:
        error_code = "gmail_not_authorized"
    elif status_code == 429:
        error_code = "gmail_rate_limit"
    elif status_code == 500:
        error_code = "gmail_api_error"
    
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=get_user_friendly_error(error_code, f"Gmail API returned {status_code}"),
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=get_user_friendly_error("internal_error", str(exc)),
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )
