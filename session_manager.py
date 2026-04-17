"""
Session management module for tracking API usage and request history
"""

import logging
from datetime import datetime
from collections import defaultdict
from typing import Dict, List

logger = logging.getLogger(__name__)


class SessionManager:
    """
    In-memory session manager for tracking user requests and API usage.
    Maintains request history per client/session.
    """
    
    def __init__(self):
        """Initialize session manager"""
        self.sessions: Dict[str, Dict] = defaultdict(lambda: {
            "requests": [],
            "created_at": datetime.now().isoformat(),
            "total_requests": 0
        })
    
    def track_request(self, client_id: str, sector: str) -> None:
        """
        Track a request for a client.
        
        Args:
            client_id: Unique identifier for the client
            sector: The sector being analyzed
        """
        session = self.sessions[client_id]
        
        request_record = {
            "timestamp": datetime.now().isoformat(),
            "sector": sector,
            "status": "completed"
        }
        
        session["requests"].append(request_record)
        session["total_requests"] += 1
        
        # Keep only last 100 requests per session
        if len(session["requests"]) > 100:
            session["requests"] = session["requests"][-100:]
        
        logger.info(f"Tracked request for client {client_id}: {sector}")
    
    def get_session_info(self, client_id: str) -> Dict:
        """
        Get session information for a client.
        
        Args:
            client_id: Unique identifier for the client
        
        Returns:
            Session information dictionary
        """
        return self.sessions.get(client_id, {
            "requests": [],
            "created_at": datetime.now().isoformat(),
            "total_requests": 0
        })
    
    def get_stats(self) -> Dict:
        """
        Get overall session statistics.
        
        Returns:
            Dictionary with session statistics
        """
        total_sessions = len(self.sessions)
        total_requests = sum(
            session["total_requests"] for session in self.sessions.values()
        )
        
        return {
            "total_sessions": total_sessions,
            "total_requests": total_requests,
            "active_clients": list(self.sessions.keys())[:10]  # Show first 10
        }
    
    def clear_old_sessions(self, max_age_hours: int = 24) -> None:
        """
        Clear sessions older than specified hours (optional cleanup).
        
        Args:
            max_age_hours: Maximum age of sessions in hours
        """
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        sessions_to_remove = []
        for client_id, session in self.sessions.items():
            created_at = datetime.fromisoformat(session["created_at"])
            if created_at < cutoff_time:
                sessions_to_remove.append(client_id)
        
        for client_id in sessions_to_remove:
            del self.sessions[client_id]
        
        if sessions_to_remove:
            logger.info(f"Cleared {len(sessions_to_remove)} old sessions")
