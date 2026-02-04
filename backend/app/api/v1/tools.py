from fastapi import APIRouter
from app.core.tools.registry import ToolRegistry
from app.dependencies import get_tool_registry

router = APIRouter()

@router.get("/tools")
def get_tools(tool_registry: ToolRegistry = Depends(get_tool_registry)):
    return tool_registry.get_tool_definitions()
