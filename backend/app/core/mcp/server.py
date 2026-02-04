from fastapi import APIRouter
from app.core.tools.registry import ToolRegistry
from app.dependencies import get_tool_registry

def create_mcp_server(tool_registry: ToolRegistry) -> APIRouter:
    router = APIRouter()

    @router.get("/tools")
    def get_tools():
        return tool_registry.get_tool_definitions()

    @router.post("/tools/{tool_name}")
    async def execute_tool(tool_name: str, tool_input: dict):
        tool = tool_registry.get_tool(tool_name)
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        return await tool.execute(session_id="mcp", **tool_input)

    return router
