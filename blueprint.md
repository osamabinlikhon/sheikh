# Agent Sheikh - Technical Blueprint

## Executive Summary

Agent Sheikh is a general-purpose AI Agent system inspired by AI Manus architecture, designed to provide autonomous task execution in isolated sandbox environments with real-time tool integration. The system leverages **Codestral** via free code completion APIs and **Ant Design X** for the user interface.

---

## 1. System Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                     (Ant Design X + Vue 3)                  │
└────────────────────────┬────────────────────────────────────┘
                         │ WebSocket + REST API
┌────────────────────────▼────────────────────────────────────┐
│                      Backend Server                          │
│                  (FastAPI + Python 3.11+)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Agent Orchestrator (PlanAct Agent)                │  │
│  │  • Session Manager (MongoDB/Redis)                   │  │
│  │  • Sandbox Controller (Docker SDK)                   │  │
│  │  • LLM Gateway (Codestral Integration)              │  │
│  │  • Tool Registry (MCP Support)                       │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ Docker API
┌────────────────────────▼────────────────────────────────────┐
│                   Sandbox Environment                        │
│                  (Ubuntu Docker Container)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Headless Chrome Browser (VNC + noVNC)            │  │
│  │  • Terminal/Shell Access (xterm.js)                 │  │
│  │  • File System Manager                              │  │
│  │  • Code Execution Environment                       │  │
│  │  • Tool API Services                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Core Components

#### **Frontend (Vue 3 + Ant Design X)**
- **Framework**: Vue 3 with Composition API
- **UI Library**: Ant Design X (AI-focused components)
- **Key Packages**:
  - `@ant-design/x` - Core AI components
  - `@ant-design/x-markdown` - Markdown rendering
  - `@ant-design/x-sdk` - SDK utilities
- **Features**:
  - Real-time chat interface with SSE
  - Tool visualization (Browser via noVNC, Terminal via xterm.js)
  - File upload/download
  - Session management
  - Dark mode support

#### **Backend (FastAPI + Python)**
- **Framework**: FastAPI 0.100+
- **Core Libraries**:
  - `fastapi` - Web framework
  - `uvicorn` - ASGI server
  - `pydantic` - Data validation
  - `motor` - Async MongoDB driver
  - `redis-py` - Redis client
  - `docker-py` - Docker SDK
  - `httpx` - Async HTTP client
- **Key Modules**:
  - `agent/` - PlanAct agent logic
  - `tools/` - Tool implementations
  - `sandbox/` - Sandbox management
  - `llm/` - Codestral integration
  - `auth/` - Authentication system

#### **Sandbox (Docker Container)**
- **Base Image**: Ubuntu 22.04
- **Services**:
  - Chrome browser with VNC access
  - Python 3.11+ runtime
  - Node.js 20+ runtime
  - File management API
  - Shell execution API
- **Networking**: Bridge network with isolated containers

---

## 2. Technology Stack

### 2.1 Frontend Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Framework** | Vue 3 | 3.4+ | Reactive UI framework |
| **UI Library** | Ant Design X | Latest | AI-specific components |
| **Build Tool** | Vite | 5.0+ | Fast development & bundling |
| **State Management** | Pinia | 2.1+ | Centralized state |
| **HTTP Client** | Axios | 1.6+ | API communication |
| **WebSocket** | Native WebSocket | - | Real-time communication |
| **Terminal** | xterm.js | 5.3+ | Terminal emulator |
| **VNC Viewer** | noVNC | 1.4+ | Browser VNC client |
| **Markdown** | @ant-design/x-markdown | Latest | Markdown rendering |
| **Code Editor** | Monaco Editor | 0.45+ | Code editing |
| **Type Checking** | TypeScript | 5.3+ | Type safety |

### 2.2 Backend Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Framework** | FastAPI | 0.100+ | Async web framework |
| **Runtime** | Python | 3.11+ | Programming language |
| **ASGI Server** | Uvicorn | 0.27+ | Production server |
| **Database** | MongoDB | 7.0+ | Document storage |
| **Cache** | Redis | 7.0+ | Session cache |
| **Container** | Docker | 20.10+ | Sandbox isolation |
| **LLM Provider** | Codestral API | - | Code generation |
| **Validation** | Pydantic | 2.5+ | Data validation |
| **Auth** | JWT | - | Authentication |
| **Email** | SMTP | - | Email notifications |

### 2.3 Sandbox Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **OS** | Ubuntu | 22.04 | Base environment |
| **Browser** | Chrome | Latest | Web automation |
| **VNC Server** | x11vnc | Latest | Screen sharing |
| **Display** | Xvfb | Latest | Virtual display |
| **WebSocket Bridge** | websockify | Latest | VNC to WebSocket |
| **Python** | Python | 3.11+ | Code execution |
| **Node.js** | Node.js | 20+ | JavaScript runtime |
| **API Server** | FastAPI | 0.100+ | Tool endpoints |

---

## 3. Feature Specifications

### 3.1 MUST-HAVE Features

#### **Core Agent Capabilities**
- **MUST** support autonomous task planning and execution via PlanAct architecture
- **MUST** integrate Codestral API for code generation and completion
- **MUST** provide function calling capabilities for tool execution
- **MUST** support JSON format output for structured responses
- **MUST** implement context management with conversation history

#### **Sandbox Management**
- **MUST** create isolated Docker containers per session
- **MUST** expose sandbox tools via REST APIs (file, shell, browser)
- **MUST** implement automatic cleanup with configurable TTL (default 30 minutes)
- **MUST** support real-time viewing of sandbox state (VNC, terminal)
- **MUST** allow user takeover for manual intervention

#### **Tool Integration**
- **MUST** implement Browser tool with Chrome automation
- **MUST** implement Terminal tool with command execution
- **MUST** implement File tool for file operations
- **MUST** implement Web Search tool (Bing/Google/Baidu)
- **MUST** support MCP (Model Context Protocol) for external tools
- **MUST** provide real-time tool output streaming

#### **Session Management**
- **MUST** persist conversation history in MongoDB
- **MUST** cache active sessions in Redis
- **MUST** support background task execution
- **MUST** enable pause/resume functionality
- **MUST** allow task interruption and cancellation

#### **User Interface**
- **MUST** use Ant Design X components for AI-specific UI
- **MUST** implement SSE for real-time message streaming
- **MUST** provide file upload/download capabilities
- **MUST** show tool execution visualization (browser, terminal)
- **MUST** support multilingual interface (English, Bengali)

#### **Authentication & Authorization**
- **MUST** implement JWT-based authentication
- **MUST** support multiple auth providers (password, local, none)
- **MUST** provide email verification for password reset
- **MUST** enforce secure password hashing (bcrypt)

### 3.2 SHOULD-HAVE Features

#### **Enhanced Capabilities**
- **SHOULD** implement rate limiting for API requests
- **SHOULD** provide usage analytics and metrics
- **SHOULD** support multi-model switching (Codestral, GPT-4, Claude)
- **SHOULD** implement cost tracking for API usage
- **SHOULD** provide export functionality for conversations

#### **Developer Features**
- **SHOULD** expose comprehensive REST API documentation
- **SHOULD** provide webhook support for event notifications
- **SHOULD** implement API versioning
- **SHOULD** support custom tool development SDK

#### **Performance & Scalability**
- **SHOULD** implement connection pooling for databases
- **SHOULD** support horizontal scaling with load balancing
- **SHOULD** cache frequent LLM responses
- **SHOULD** implement lazy loading for large file lists

### 3.3 NEVER Requirements

#### **Security Prohibitions**
- **NEVER** expose Docker socket to untrusted users
- **NEVER** store API keys in plaintext
- **NEVER** allow arbitrary code execution outside sandbox
- **NEVER** bypass authentication for sensitive endpoints
- **NEVER** log sensitive user data (passwords, API keys)

#### **Architecture Constraints**
- **NEVER** create tight coupling between frontend and backend
- **NEVER** use synchronous operations for long-running tasks
- **NEVER** store large files in database (use object storage)
- **NEVER** allow unbounded resource allocation in sandboxes
- **NEVER** implement client-side security validation only

---

## 4. Implementation Guidelines

### 4.1 Frontend Implementation

#### **4.1.1 Project Structure**
```
frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatInterface.vue       # Main chat component
│   │   │   ├── MessageList.vue         # Message display
│   │   │   ├── InputBox.vue            # User input
│   │   │   └── ToolViewer.vue          # Tool visualization
│   │   ├── tools/
│   │   │   ├── BrowserViewer.vue       # noVNC integration
│   │   │   ├── TerminalViewer.vue      # xterm.js integration
│   │   │   ├── FileManager.vue         # File operations
│   │   │   └── CodeEditor.vue          # Monaco editor
│   │   └── layout/
│   │       ├── AppHeader.vue
│   │       ├── AppSidebar.vue
│   │       └── AppFooter.vue
│   ├── stores/
│   │   ├── auth.ts                     # Auth state
│   │   ├── session.ts                  # Session state
│   │   └── tools.ts                    # Tool state
│   ├── services/
│   │   ├── api.ts                      # API client
│   │   ├── websocket.ts                # WebSocket client
│   │   └── sse.ts                      # SSE client
│   ├── utils/
│   │   ├── markdown.ts                 # Markdown utilities
│   │   └── format.ts                   # Formatting helpers
│   ├── types/
│   │   ├── api.ts                      # API types
│   │   └── models.ts                   # Data models
│   ├── locales/
│   │   ├── en.json                     # English translations
│   │   └── bn.json                     # Bengali translations
│   ├── App.vue
│   └── main.ts
├── package.json
├── vite.config.ts
└── tsconfig.json
```

#### **4.1.2 Ant Design X Integration**
```typescript
// main.ts
import { createApp } from 'vue';
import App from './App.vue';
import { 
  Bubble, 
  Conversations, 
  Prompts, 
  Sender,
  useXAgent,
  useXChat
} from '@ant-design/x';
import '@ant-design/x/dist/index.css';

const app = createApp(App);

// Register Ant Design X components
app.component('Bubble', Bubble);
app.component('Conversations', Conversations);
app.component('Prompts', Prompts);
app.component('Sender', Sender);

app.mount('#app');
```

#### **4.1.3 Chat Interface Component**
```vue
<!-- ChatInterface.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useXChat } from '@ant-design/x';
import { Bubble, Sender } from '@ant-design/x';
import { SSEClient } from '@/services/sse';

const { messages, sendMessage } = useXChat();
const sseClient = ref<SSEClient | null>(null);

onMounted(() => {
  sseClient.value = new SSEClient('/api/chat/stream');
  sseClient.value.onMessage((data) => {
    // Handle streaming messages
    messages.value.push(data);
  });
});

const handleSend = async (content: string) => {
  await sendMessage(content);
};
</script>

<template>
  <div class="chat-interface">
    <Bubble 
      v-for="msg in messages" 
      :key="msg.id"
      :content="msg.content"
      :role="msg.role"
    />
    <Sender 
      @send="handleSend"
      placeholder="Ask Agent Sheikh anything..."
    />
  </div>
</template>
```

### 4.2 Backend Implementation

#### **4.2.1 Project Structure**
```
backend/
├── app/
│   ├── main.py                         # FastAPI app entry
│   ├── config.py                       # Configuration
│   ├── dependencies.py                 # Dependency injection
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py                 # Auth endpoints
│   │   │   ├── chat.py                 # Chat endpoints
│   │   │   ├── sessions.py             # Session endpoints
│   │   │   ├── tools.py                # Tool endpoints
│   │   │   └── sandbox.py              # Sandbox endpoints
│   │   └── deps.py                     # API dependencies
│   ├── core/
│   │   ├── agent/
│   │   │   ├── base.py                 # Base agent class
│   │   │   ├── planact.py              # PlanAct agent
│   │   │   └── executor.py             # Tool executor
│   │   ├── llm/
│   │   │   ├── base.py                 # LLM interface
│   │   │   ├── codestral.py            # Codestral client
│   │   │   └── function_calling.py     # Function call handler
│   │   ├── tools/
│   │   │   ├── base.py                 # Tool interface
│   │   │   ├── browser.py              # Browser tool
│   │   │   ├── terminal.py             # Terminal tool
│   │   │   ├── file.py                 # File tool
│   │   │   ├── search.py               # Search tool
│   │   │   └── registry.py             # Tool registry
│   │   ├── sandbox/
│   │   │   ├── manager.py              # Sandbox manager
│   │   │   ├── docker_client.py        # Docker integration
│   │   │   └── lifecycle.py            # Lifecycle management
│   │   └── mcp/
│   │       ├── client.py               # MCP client
│   │       └── server.py               # MCP server
│   ├── models/
│   │   ├── user.py                     # User model
│   │   ├── session.py                  # Session model
│   │   ├── message.py                  # Message model
│   │   └── tool.py                     # Tool model
│   ├── schemas/
│   │   ├── auth.py                     # Auth schemas
│   │   ├── chat.py                     # Chat schemas
│   │   └── tool.py                     # Tool schemas
│   ├── services/
│   │   ├── auth.py                     # Auth service
│   │   ├── session.py                  # Session service
│   │   └── email.py                    # Email service
│   └── utils/
│       ├── crypto.py                   # Encryption utilities
│       ├── logging.py                  # Logging setup
│       └── validators.py               # Custom validators
├── requirements.txt
├── Dockerfile
└── pytest.ini
```

#### **4.2.2 Codestral Integration**
```python
# app/core/llm/codestral.py
from typing import AsyncGenerator, Dict, List, Optional
import httpx
from pydantic import BaseModel

class CodestralClient:
    """Client for Codestral API via code completion endpoint."""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.mistral.ai/v1",
        model: str = "codestral-latest"
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0
        )
    
    async def complete(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        stop: Optional[List[str]] = None,
        tools: Optional[List[Dict]] = None
    ) -> Dict:
        """Generate code completion with optional function calling."""
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stop": stop or []
        }
        
        # Add function calling support if tools provided
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        response = await self.client.post(
            f"{self.base_url}/completions",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def stream_complete(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """Stream code completion responses."""
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True
        }
        
        async with self.client.stream(
            "POST",
            f"{self.base_url}/completions",
            json=payload
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    yield line[6:]  # Remove "data: " prefix
```

#### **4.2.3 PlanAct Agent Implementation**
```python
# app/core/agent/planact.py
from typing import List, AsyncGenerator
from .base import BaseAgent
from ..llm.codestral import CodestralClient
from ..tools.registry import ToolRegistry

class PlanActAgent(BaseAgent):
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
        plan_response = await self.llm.complete(
            prompt=plan_prompt,
            tools=self.tools.get_tool_definitions()
        )
        
        yield {
            "type": "plan",
            "content": plan_response["choices"][0]["text"]
        }
        
        # Execute tools based on plan
        iteration = 0
        while iteration < self.max_iterations:
            # Check if task is complete
            if self._is_task_complete(plan_response):
                break
            
            # Execute tool calls
            tool_calls = self._extract_tool_calls(plan_response)
            for tool_call in tool_calls:
                tool_result = await self._execute_tool(
                    tool_call,
                    session_id
                )
                
                yield {
                    "type": "tool_execution",
                    "tool": tool_call["name"],
                    "result": tool_result
                }
            
            # Reflect and adjust plan
            reflection_prompt = self._create_reflection_prompt(
                user_message,
                tool_calls,
                [r["result"] for r in tool_results]
            )
            
            plan_response = await self.llm.complete(
                prompt=reflection_prompt,
                tools=self.tools.get_tool_definitions()
            )
            
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
    
    async def _execute_tool(
        self,
        tool_call: Dict,
        session_id: str
    ) -> Dict:
        """Execute a single tool call."""
        tool = self.tools.get_tool(tool_call["name"])
        return await tool.execute(
            session_id=session_id,
            **tool_call["arguments"]
        )
```

### 4.3 Sandbox Implementation

#### **4.3.1 Sandbox Manager**
```python
# app/core/sandbox/manager.py
import docker
from typing import Dict, Optional
from datetime import datetime, timedelta

class SandboxManager:
    """Manages Docker sandbox containers for isolated execution."""
    
    def __init__(
        self,
        docker_client: docker.DockerClient,
        image: str = "agent-sheikh-sandbox:latest",
        network: str = "agent-sheikh-network",
        ttl_minutes: int = 30
    ):
        self.docker = docker_client
        self.image = image
        self.network = network
        self.ttl = timedelta(minutes=ttl_minutes)
        self.active_sandboxes: Dict[str, Dict] = {}
    
    async def create_sandbox(self, session_id: str) -> Dict:
        """Create a new sandbox container for a session."""
        
        container_name = f"sheikh-sandbox-{session_id}"
        
        # Create container
        container = self.docker.containers.run(
            image=self.image,
            name=container_name,
            network=self.network,
            detach=True,
            remove=False,
            environment={
                "SESSION_ID": session_id,
                "DISPLAY": ":99"
            },
            cap_add=["SYS_ADMIN"],  # For Chrome
            shm_size="2g",  # Shared memory for Chrome
            mem_limit="2g",
            cpu_period=100000,
            cpu_quota=150000,  # 1.5 CPU cores
        )
        
        # Wait for services to start
        await self._wait_for_services(container)
        
        # Register sandbox
        self.active_sandboxes[session_id] = {
            "container": container,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + self.ttl
        }
        
        return {
            "session_id": session_id,
            "container_id": container.id,
            "vnc_port": 5900,
            "api_port": 8080,
            "status": "ready"
        }
    
    async def destroy_sandbox(self, session_id: str) -> None:
        """Destroy a sandbox container."""
        
        if session_id not in self.active_sandboxes:
            return
        
        container = self.active_sandboxes[session_id]["container"]
        container.stop(timeout=10)
        container.remove()
        
        del self.active_sandboxes[session_id]
    
    async def cleanup_expired_sandboxes(self) -> None:
        """Remove expired sandbox containers."""
        
        now = datetime.utcnow()
        expired = [
            sid for sid, info in self.active_sandboxes.items()
            if info["expires_at"] < now
        ]
        
        for session_id in expired:
            await self.destroy_sandbox(session_id)
```

#### **4.3.2 Sandbox Dockerfile**
```dockerfile
# sandbox/Dockerfile
FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    nodejs \
    npm \
    xvfb \
    x11vnc \
    websockify \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Setup working directory
WORKDIR /workspace

# Copy sandbox API server
COPY sandbox_api/ /app/
WORKDIR /app

# Expose ports
EXPOSE 8080 5900

# Start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
```

#### **4.3.3 Sandbox Startup Script**
```bash
#!/bin/bash
# sandbox/start.sh

# Start virtual display
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99

# Start VNC server
x11vnc -display :99 -forever -shared -rfbport 5900 &

# Start websockify for VNC over WebSocket
websockify --web /usr/share/novnc 6080 localhost:5900 &

# Start Chrome in headless mode
google-chrome-stable \
    --headless \
    --disable-gpu \
    --remote-debugging-port=9222 \
    --no-sandbox \
    --disable-dev-shm-usage &

# Start sandbox API server
cd /app
uvicorn main:app --host 0.0.0.0 --port 8080
```

---

## 5. Configuration Specifications

### 5.1 Environment Variables

```bash
# LLM Configuration
API_KEY=                                    # Codestral API key
API_BASE=https://api.mistral.ai/v1         # Codestral base URL
MODEL_NAME=codestral-latest                # Model identifier
TEMPERATURE=0.7                            # Sampling temperature
MAX_TOKENS=2000                            # Max response tokens

# Database Configuration
MONGODB_URI=mongodb://mongodb:27017        # MongoDB connection string
MONGODB_DATABASE=agent_sheikh              # Database name
MONGODB_USERNAME=                          # Optional username
MONGODB_PASSWORD=                          # Optional password

# Cache Configuration
REDIS_HOST=redis                           # Redis hostname
REDIS_PORT=6379                            # Redis port
REDIS_DB=0                                 # Redis database number
REDIS_PASSWORD=                            # Optional password

# Sandbox Configuration
SANDBOX_IMAGE=agent-sheikh-sandbox:latest  # Docker image
SANDBOX_NAME_PREFIX=sheikh-sandbox         # Container name prefix
SANDBOX_TTL_MINUTES=30                     # Time-to-live in minutes
SANDBOX_NETWORK=agent-sheikh-network       # Docker network
SANDBOX_HTTPS_PROXY=                       # Optional HTTPS proxy
SANDBOX_HTTP_PROXY=                        # Optional HTTP proxy
SANDBOX_NO_PROXY=                          # No proxy hosts

# Search Configuration
SEARCH_PROVIDER=bing                       # bing|google|baidu
GOOGLE_SEARCH_API_KEY=                     # Google API key
GOOGLE_SEARCH_ENGINE_ID=                   # Google Search Engine ID

# Authentication Configuration
AUTH_PROVIDER=password                     # password|none|local
PASSWORD_SALT=                             # Password salt
PASSWORD_HASH_ROUNDS=10                    # Bcrypt rounds
LOCAL_AUTH_EMAIL=admin@example.com         # Local admin email
LOCAL_AUTH_PASSWORD=admin                  # Local admin password

# JWT Configuration
JWT_SECRET_KEY=                            # Secret for JWT signing
JWT_ALGORITHM=HS256                        # Signing algorithm
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30         # Access token TTL
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7            # Refresh token TTL

# Email Configuration
EMAIL_HOST=smtp.gmail.com                  # SMTP host
EMAIL_PORT=587                             # SMTP port
EMAIL_USERNAME=                            # SMTP username
EMAIL_PASSWORD=                            # SMTP password
EMAIL_FROM=                                # From address

# MCP Configuration
MCP_CONFIG_PATH=/etc/mcp.json              # MCP config file path

# Logging Configuration
LOG_LEVEL=INFO                             # DEBUG|INFO|WARNING|ERROR
```

### 5.2 Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    image: agent-sheikh-frontend:latest
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:80"
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:8000
    networks:
      - agent-sheikh-network
    restart: unless-stopped