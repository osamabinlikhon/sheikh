from pydantic import BaseModel
from typing import List, Dict

class Session(BaseModel):
    session_id: str
    conversation_history: List[Dict] = []
    sandbox_id: str | None = None
