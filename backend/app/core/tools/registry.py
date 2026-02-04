from typing import Dict, List
from .base import BaseTool
from .browser import BrowserTool
from .terminal import TerminalTool
from .file import FileTool
from .search import SearchTool

class ToolRegistry:
    def __init__(self):
        self._tools = {
            "browser": BrowserTool(),
            "terminal": TerminalTool(),
            "file": FileTool(),
            "search": SearchTool(),
        }

    def get_tool(self, name: str) -> BaseTool:
        return self._tools.get(name)

    def get_tool_definitions(self) -> List[Dict]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            }
            for tool in self._tools.values()
        ]
