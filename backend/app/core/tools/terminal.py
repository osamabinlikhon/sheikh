from .base import BaseTool
import asyncio

class TerminalTool(BaseTool):
    @property
    def name(self) -> str:
        return "terminal"

    @property
    def description(self) -> str:
        return "A tool for executing shell commands."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to execute."
                }
            },
            "required": ["command"]
        }

    async def execute(self, session_id: str, **kwargs) -> dict:
        # This is a placeholder. In a real implementation, this would
        # execute the command in the sandbox.
        proc = await asyncio.create_subprocess_shell(
            kwargs["command"],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "exit_code": proc.returncode
        }
