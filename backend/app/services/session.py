from typing import Dict, List
from app.models.session import Session

class SessionService:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def create_session(self, session_id: str) -> Session:
        session = Session(session_id=session_id)
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Session | None:
        return self.sessions.get(session_id)

    def update_session_history(self, session_id: str, message: Dict):
        session = self.get_session(session_id)
        if session:
            session.conversation_history.append(message)
            self.sessions[session_id] = session

    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
