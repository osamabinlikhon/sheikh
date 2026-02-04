from pydantic import BaseModel
from typing import Dict, Any

class ToolSchema(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
