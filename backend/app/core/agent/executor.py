from typing import Dict
from app.core.tools.registry import ToolRegistry

class ToolExecutor:
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    async def execute_tool(self, tool_call: Dict, session_id: str) -> Dict:
        """Executes a tool call."""
        tool_name = tool_call["name"]
        tool_args = tool_call["arguments"]
        tool = self.tool_registry.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found.")
        return await tool.execute(session_id=session_id, **tool_args)
