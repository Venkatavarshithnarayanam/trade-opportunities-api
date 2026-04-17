"""
Authentication module for API key validation
"""

import os
import logging

logger = logging.getLogger(__name__)

# Default API key for development/testing
DEFAULT_API_KEY = "trade-api-key-2024"


def get_valid_api_keys() -> list[str]:
    """
    Get list of valid API keys from environment or defaults.
    
    Returns:
        List of valid API keys
    """
    env_keys = os.getenv("VALID_API_KEYS", "")
    if env_keys:
        return [key.strip() for key in env_keys.split(",") if key.strip()]
    return [DEFAULT_API_KEY]


def verify_api_key(api_key: str) -> bool:
    """
    Verify if the provided API key is valid.
    
    Args:
        api_key: The API key to verify
    
    Returns:
        True if valid, False otherwise
    """
    if not api_key:
        return False
    
    valid_keys = get_valid_api_keys()
    is_valid = api_key in valid_keys
    
    if not is_valid:
        logger.debug(f"Invalid API key attempt: {api_key[:10]}...")
    
    return is_valid
