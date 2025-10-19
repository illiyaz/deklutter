"""
Provider-specific configuration for rate limiting, retries, and circuit breakers

Each provider (Gmail, Yahoo, Outlook, etc.) has different API limits and requirements.
This file centralizes all provider-specific configurations.
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class ProviderConfig:
    """Configuration for a specific email provider"""
    
    # Provider identification
    name: str
    display_name: str
    
    # Rate limiting
    max_emails_per_scan: int
    batch_size: int
    rate_limit_delay: float  # seconds between batches
    
    # Retry configuration
    max_retries: int
    retry_delay: float  # base delay in seconds
    retry_on_status_codes: list[int]  # HTTP status codes to retry
    
    # Circuit breaker configuration
    circuit_breaker_failure_threshold: int
    circuit_breaker_timeout: int  # seconds
    circuit_breaker_success_threshold: int
    
    # API quota information (for documentation)
    daily_quota: str
    quota_per_second: str
    notes: str

# Provider configurations
PROVIDER_CONFIGS: Dict[str, ProviderConfig] = {
    "gmail": ProviderConfig(
        name="gmail",
        display_name="Gmail",
        
        # Rate limiting
        max_emails_per_scan=1000,
        batch_size=100,  # Gmail allows up to 100 in batch request
        rate_limit_delay=0.1,  # 100ms between batches
        
        # Retry configuration
        max_retries=3,
        retry_delay=2.0,
        retry_on_status_codes=[429, 500, 503],  # Rate limit, server error, unavailable
        
        # Circuit breaker
        circuit_breaker_failure_threshold=5,
        circuit_breaker_timeout=60,
        circuit_breaker_success_threshold=2,
        
        # API quota info
        daily_quota="1 billion quota units/day",
        quota_per_second="250 quota units/second/user",
        notes="messages.list: 5 units, messages.get: 5 units. Batch requests highly recommended."
    ),
    
    "yahoo": ProviderConfig(
        name="yahoo",
        display_name="Yahoo Mail",
        
        # Rate limiting (Yahoo is more restrictive)
        max_emails_per_scan=500,
        batch_size=50,  # Yahoo has smaller batch limits
        rate_limit_delay=0.2,  # 200ms between batches (more conservative)
        
        # Retry configuration
        max_retries=3,
        retry_delay=3.0,  # Longer delay for Yahoo
        retry_on_status_codes=[429, 500, 503],
        
        # Circuit breaker (more sensitive for Yahoo)
        circuit_breaker_failure_threshold=3,  # Open faster
        circuit_breaker_timeout=120,  # Wait longer before retry
        circuit_breaker_success_threshold=3,  # Need more successes
        
        # API quota info
        daily_quota="~10,000 requests/day (estimated)",
        quota_per_second="~10 requests/second (estimated)",
        notes="Yahoo Mail API has stricter rate limits. Use conservative settings."
    ),
    
    "outlook": ProviderConfig(
        name="outlook",
        display_name="Outlook/Microsoft 365",
        
        # Rate limiting
        max_emails_per_scan=1000,
        batch_size=20,  # Microsoft Graph batch limit
        rate_limit_delay=0.15,  # 150ms between batches
        
        # Retry configuration
        max_retries=3,
        retry_delay=2.0,
        retry_on_status_codes=[429, 500, 503, 504],  # Include gateway timeout
        
        # Circuit breaker
        circuit_breaker_failure_threshold=5,
        circuit_breaker_timeout=60,
        circuit_breaker_success_threshold=2,
        
        # API quota info
        daily_quota="Varies by license (typically 10,000-50,000 requests/day)",
        quota_per_second="~20 requests/second",
        notes="Microsoft Graph API. Batch limit is 20 requests. Throttling is per-user."
    ),
    
    # Template for future providers
    "template": ProviderConfig(
        name="template",
        display_name="Provider Template",
        
        # Rate limiting
        max_emails_per_scan=500,  # Conservative default
        batch_size=50,
        rate_limit_delay=0.2,
        
        # Retry configuration
        max_retries=3,
        retry_delay=2.0,
        retry_on_status_codes=[429, 500, 503],
        
        # Circuit breaker
        circuit_breaker_failure_threshold=5,
        circuit_breaker_timeout=60,
        circuit_breaker_success_threshold=2,
        
        # API quota info
        daily_quota="Unknown",
        quota_per_second="Unknown",
        notes="Update this configuration based on provider's API documentation."
    )
}

def get_provider_config(provider_name: str) -> ProviderConfig:
    """Get configuration for a specific provider"""
    provider_name = provider_name.lower()
    
    if provider_name not in PROVIDER_CONFIGS:
        raise ValueError(f"Unknown provider: {provider_name}. Available: {list(PROVIDER_CONFIGS.keys())}")
    
    return PROVIDER_CONFIGS[provider_name]

def list_providers() -> list[str]:
    """List all configured providers"""
    return [name for name in PROVIDER_CONFIGS.keys() if name != "template"]

def get_all_configs() -> Dict[str, ProviderConfig]:
    """Get all provider configurations (excluding template)"""
    return {k: v for k, v in PROVIDER_CONFIGS.items() if k != "template"}

# Auto-generate RESILIENCE.md section
def generate_resilience_docs() -> str:
    """Generate provider-specific section for RESILIENCE.md"""
    docs = "## 📊 Provider-Specific Configurations\n\n"
    docs += "_Auto-generated from `services/connectors/provider_config.py`_\n\n"
    
    for name, config in get_all_configs().items():
        docs += f"### **{config.display_name}**\n\n"
        docs += f"**Rate Limiting:**\n"
        docs += f"- Max emails per scan: {config.max_emails_per_scan}\n"
        docs += f"- Batch size: {config.batch_size}\n"
        docs += f"- Delay between batches: {config.rate_limit_delay}s\n\n"
        
        docs += f"**Retry Configuration:**\n"
        docs += f"- Max retries: {config.max_retries}\n"
        docs += f"- Base delay: {config.retry_delay}s (exponential backoff)\n"
        docs += f"- Retry on: {config.retry_on_status_codes}\n\n"
        
        docs += f"**Circuit Breaker:**\n"
        docs += f"- Failure threshold: {config.circuit_breaker_failure_threshold}\n"
        docs += f"- Timeout: {config.circuit_breaker_timeout}s\n"
        docs += f"- Success threshold: {config.circuit_breaker_success_threshold}\n\n"
        
        docs += f"**API Quotas:**\n"
        docs += f"- Daily: {config.daily_quota}\n"
        docs += f"- Per second: {config.quota_per_second}\n"
        docs += f"- Notes: {config.notes}\n\n"
        docs += "---\n\n"
    
    return docs

if __name__ == "__main__":
    # Generate and print provider docs
    print(generate_resilience_docs())
