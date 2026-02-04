from pydantic import BaseModel
from typing import Dict

class Tool(BaseModel):
    name: str
    description: str
    parameters: Dict
