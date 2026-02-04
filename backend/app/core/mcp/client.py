import httpx

class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def get_tools(self):
        response = await self.client.get(f"{self.base_url}/tools")
        response.raise_for_status()
        return response.json()

    async def execute_tool(self, tool_name: str, **kwargs):
        response = await self.client.post(
            f"{self.base_url}/tools/{tool_name}",
            json=kwargs
        )
        response.raise_for_status()
        return response.json()
