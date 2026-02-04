from .base import BaseTool
import os

class FileTool(BaseTool):
    @property
    def name(self) -> str:
        return "file"

    @property
    def description(self) -> str:
        return "A tool for file operations."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "The file operation to perform.",
                    "enum": ["read", "write", "list"]
                },
                "path": {
                    "type": "string",
                    "description": "The path to the file or directory."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file."
                }
            },
            "required": ["operation", "path"]
        }

    async def execute(self, session_id: str, **kwargs) -> dict:
        # This is a placeholder. In a real implementation, this would
        # perform the file operation in the sandbox.
        operation = kwargs["operation"]
        path = kwargs["path"]
        if operation == "read":
            with open(path, "r") as f:
                content = f.read()
            return {"content": content}
        elif operation == "write":
            content = kwargs["content"]
            with open(path, "w") as f:
                f.write(content)
            return {"status": "ok"}
        elif operation == "list":
            return {"files": os.listdir(path)}
        else:
            raise ValueError(f"Unknown operation: {operation}")
