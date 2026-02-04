from typing import List, AsyncGenerator, Dict, Any, Optional
from loguru import logger

from app.core.llm.codestral import CodestralClient
from app.core.tools.registry import ToolRegistry


class PlanActAgent:
    """
    PlanAct agent that plans tasks and executes using available tools.
    
    Architecture:
    1. Plan: Generate execution plan from user request
    2. Act: Execute tools according to plan
    3. Observe: Collect tool outputs
    4. Reflect: Evaluate progress and adjust plan
    """
    
    def __init__(
        self,
        llm_client: CodestralClient,
        tool_registry: ToolRegistry,
        max_iterations: int = 10
    ):
        self.llm = llm_client
        self.tools = tool_registry
        self.max_iterations = max_iterations
        self.conversation_history: List[Dict] = []
    
    async def run(
        self,
        user_message: str,
        session_id: str
    ) -> AsyncGenerator[Dict, None]:
        """Execute agent loop with streaming outputs."""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Generate initial plan
        plan_prompt = self._create_plan_prompt(user_message)
        plan_response = await self.llm.chat_complete(
            messages=self.conversation_history,
            tools=self.tools.get_tool_definitions()
        )
        
        plan_content = self._extract_plan_content(plan_response)
        yield {
            "type": "plan",
            "content": plan_content
        }
        
        # Execute tools based on plan
        iteration = 0
        tool_results = []
        
        while iteration < self.max_iterations:
            # Check if task is complete
            if self._is_task_complete(plan_response):
                break
            
            # Extract and execute tool calls
            tool_calls = self._extract_tool_calls(plan_response)
            
            for tool_call in tool_calls:
                try:
                    tool_result = await self._execute_tool(
                        tool_call,
                        session_id
                    )
                    
                    yield {
                        "type": "tool_execution",
                        "tool": tool_call["name"],
                        "arguments": tool_call["arguments"],
                        "result": tool_result
                    }
                    
                    tool_results.append(tool_result)
                    
                except Exception as e:
                    logger.error(f"Tool execution failed: {e}")
                    yield {
                        "type": "tool_error",
                        "tool": tool_call["name"],
                        "error": str(e)
                    }
            
            # Reflect and adjust plan
            reflection_prompt = self._create_reflection_prompt(
                user_message,
                tool_calls,
                tool_results
            )
            
            self.conversation_history.append({
                "role": "assistant",
                "content": plan_content,
                "tool_calls": tool_calls
            })
            
            # Add tool results to history
            for result in tool_results:
                self.conversation_history.append({
                    "role": "tool",
                    "content": result,
                    "name": "tool_result"
                })
            
            # Get new plan
            plan_response = await self.llm.chat_complete(
                messages=self.conversation_history,
                tools=self.tools.get_tool_definitions()
            )
            
            plan_content = self._extract_plan_content(plan_response)
            yield {
                "type": "reflection",
                "content": plan_content
            }
            
            iteration += 1
        
        # Generate final response
        final_response = self._format_final_response(plan_response)
        self.conversation_history.append({
            "role": "assistant",
            "content": final_response
        })
        
        yield {
            "type": "completion",
            "content": final_response
        }
    
    def _create_plan_prompt(self, user_message: str) -> str:
        """Create prompt for initial planning."""
        return f"""You are Agent Sheikh, an AI assistant that can use various tools.

Available Tools:
{self.tools.get_tool_descriptions()}

User Request: {user_message}

Create a step-by-step plan to accomplish this task. Use function calls when needed."""
    
    def _create_reflection_prompt(
        self,
        user_message: str,
        tool_calls: List[Dict],
        tool_results: List[Dict]
    ) -> str:
        """Create prompt for reflection and plan adjustment."""
        
        results_str = "\n".join([
            f"- {result.get('tool', 'unknown')}: {result.get('result', 'no result')}"
            for result in tool_results
        ])
        
        return f"""You are Agent Sheikh, an AI assistant.

User Request: {user_message}

Previous tool calls and results:
{results_str}

Evaluate the progress and create an updated plan. What should be done next?"""
    
    async def _execute_tool(
        self,
        tool_call: Dict,
        session_id: str
    ) -> Dict:
        """Execute a single tool call."""
        
        tool_name = tool_call["name"]
        arguments = tool_call["arguments"]
        
        # Add session_id to arguments
        arguments["session_id"] = session_id
        
        try:
            result = await self.tools.execute_tool(tool_name, **arguments)
            return result
        except Exception as e:
            return {
                "tool": tool_name,
                "result": str(e),
                "status": "error"
            }
    
    def _extract_tool_calls(self, response: Dict) -> List[Dict]:
        """Extract tool calls from LLM response."""
        
        tool_calls = []
        
        if "choices" in response and response["choices"]:
            message = response["choices"][0].get("message", {})
            
            if "tool_calls" in message:
                for tool_call in message["tool_calls"]:
                    tool_calls.append({
                        "name": tool_call["function"]["name"],
                        "arguments": tool_call["function"]["arguments"]
                    })
        
        return tool_calls
    
    def _extract_plan_content(self, response: Dict) -> str:
        """Extract plan content from LLM response."""
        
        if "choices" in response and response["choices"]:
            return response["choices"][0].get("message", {}).get("content", "")
        
        return ""
    
    def _is_task_complete(self, response: Dict) -> bool:
        """Check if the task is complete based on LLM response."""
        
        content = self._extract_plan_content(response)
        
        # Check for completion indicators
        completion_indicators = [
            "task completed",
            "completed successfully",
            "finished",
            "done",
            "accomplished"
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in completion_indicators)
    
    def _format_final_response(self, response: Dict) -> str:
        """Format final response for user."""
        
        return self._extract_plan_content(response)
    
    def get_conversation_history(self) -> List[Dict]:
        """Get current conversation history."""
        return self.conversation_history.copy()
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []