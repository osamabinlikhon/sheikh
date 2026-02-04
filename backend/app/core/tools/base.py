from abc import ABC, abstractmethod
from typing import Dict

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict:
        pass

    @abstractmethod
    async def execute(self, session_id: str, **kwargs) -> Dict:
        pass
