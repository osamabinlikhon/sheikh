from typing import Dict, Optional
from datetime import datetime, timedelta

class SandboxLifecycle:
    """Manages the lifecycle of a sandbox."""

    def __init__(self, ttl_minutes: int = 30):
        self.ttl = timedelta(minutes=ttl_minutes)
        self.active_sandboxes: Dict[str, Dict] = {}

    def register_sandbox(self, session_id: str, container: 'docker.models.containers.Container'):
        """Registers a new sandbox."""
        self.active_sandboxes[session_id] = {
            "container": container,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + self.ttl,
        }

    def unregister_sandbox(self, session_id: str):
        """Unregisters a sandbox."""
        if session_id in self.active_sandboxes:
            del self.active_sandboxes[session_id]

    def get_expired_sandboxes(self) -> list[str]:
        """Returns a list of expired sandbox session IDs."""
        now = datetime.utcnow()
        return [
            sid
            for sid, info in self.active_sandboxes.items()
            if info["expires_at"] < now
        ]
