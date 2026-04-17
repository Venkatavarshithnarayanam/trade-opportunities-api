"""
Rate limiting module for API request throttling
Implements token bucket algorithm for per-client rate limiting
"""

import time
import logging
from collections import defaultdict
from typing import Dict

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    In-memory rate limiter using token bucket algorithm.
    Tracks requests per client/IP and enforces rate limits.
    """
    
    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """
        Check if a client is allowed to make a request.
        
        Args:
            client_id: Unique identifier for the client
        
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        current_time = time.time()
        window_start = current_time - self.window_seconds
        
        # Clean old requests outside the window
        self.clients[client_id] = [
            req_time for req_time in self.clients[client_id]
            if req_time > window_start
        ]
        
        # Check if limit exceeded
        if len(self.clients[client_id]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            return False
        
        # Add current request
        self.clients[client_id].append(current_time)
        return True
    
    def get_remaining_requests(self, client_id: str) -> int:
        """
        Get remaining requests for a client in current window.
        
        Args:
            client_id: Unique identifier for the client
        
        Returns:
            Number of remaining requests
        """
        current_time = time.time()
        window_start = current_time - self.window_seconds
        
        recent_requests = [
            req_time for req_time in self.clients[client_id]
            if req_time > window_start
        ]
        
        return max(0, self.max_requests - len(recent_requests))
