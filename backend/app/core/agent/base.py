from abc import ABC, abstractmethod
from typing import AsyncGenerator

class BaseAgent(ABC):
    @abstractmethod
    async def run(self, user_message: str, session_id: str) -> AsyncGenerator[dict, None]:
        pass
