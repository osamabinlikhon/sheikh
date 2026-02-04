from typing import AsyncGenerator, Dict, List, Optional, Any
import httpx
from pydantic import BaseModel, Field
from loguru import logger

from app.config import settings


class CodestralClient:
    """Client for Codestral API via code completion endpoint."""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = None,
        model: str = None
    ):
        self.api_key = api_key
        self.base_url = base_url or settings.api_base
        self.model = model or settings.model_name
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=60.0
        )
    
    async def complete(
        self,
        prompt: str,
        max_tokens: int = None,
        temperature: float = None,
        stop: Optional[List[str]] = None,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[str] = None
    ) -> Dict:
        """Generate code completion with optional function calling."""
        
        max_tokens = max_tokens or settings.max_tokens
        temperature = temperature or settings.temperature
        
        # Use chat completions endpoint as specified in blueprint
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        # Add function calling support if tools provided
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = tool_choice or "auto"
        
        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error calling Codestral API: {e}")
            raise
    
    async def stream_complete(
        self,
        prompt: str,
        max_tokens: int = None,
        temperature: float = None
    ) -> AsyncGenerator[str, None]:
        """Stream code completion responses."""
        
        max_tokens = max_tokens or settings.max_tokens
        temperature = temperature or settings.temperature
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True
        }
        
        try:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=payload
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        yield line[6:]  # Remove "data: " prefix
                    elif line == "data: [DONE]":
                        break
        except httpx.HTTPError as e:
            logger.error(f"Error streaming from Codestral API: {e}")
            raise
    
    async def chat_complete(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = None,
        temperature: float = None,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[str] = None
    ) -> Dict:
        """Generate chat completion with conversation history."""
        
        max_tokens = max_tokens or settings.max_tokens
        temperature = temperature or settings.temperature
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        # Add function calling support if tools provided
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = tool_choice or "auto"
        
        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error calling Codestral chat API: {e}")
            raise
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


class FunctionCall(BaseModel):
    """Function call schema for tool execution."""
    
    name: str = Field(..., description="Name of the function to call")
    arguments: Dict[str, Any] = Field(..., description="Arguments for the function")
    description: Optional[str] = Field(None, description="Description of the function")


class ToolDefinition(BaseModel):
    """Tool definition for function calling."""
    
    type: str = "function"
    function: FunctionCall