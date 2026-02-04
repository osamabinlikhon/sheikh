# Agent Sheikh - Sandbox Environment

The Sandbox is an isolated Docker container where the AI agent executes tasks. It provides a secure, controlled environment with access to a browser, terminal, and file system.

## Features

- **Isolated Execution**: Each session runs in its own container to prevent side effects and ensure security.
- **GUI Access**: Includes a virtual display (Xvfb) and VNC server for viewing browser activity.
- **Web Automation**: Headless Chrome pre-installed for web scraping and automation tasks.
- **Development Runtimes**: Pre-configured with Python 3.11 and Node.js.
- **Tool API**: Internal API server to expose container capabilities to the agent orchestrator.

## Tech Stack

- **Base OS**: Ubuntu 22.04
- **Browser**: Google Chrome
- **Display**: Xvfb (Virtual Framebuffer)
- **VNC**: x11vnc & websockify (noVNC support)
- **API Server**: FastAPI

## Components

- `Dockerfile`: Defines the sandbox environment and its dependencies.
- `sandbox_api/`: FastAPI application that runs inside the container to provide tool endpoints.
- `start.sh`: Entry point script that initializes the virtual display, VNC server, and API services.
- `sandbox_requirements.txt`: Python dependencies for the internal sandbox API.

## Building the Sandbox Image

The sandbox image is typically built automatically by the backend or via docker-compose. To build it manually:

```bash
cd sandbox
docker build -t agent-sheikh-sandbox:latest .
```

## Security Considerations

- **Resource Limits**: Sandboxes should be run with CPU and memory limits.
- **Network Isolation**: It is recommended to run sandboxes on a restricted Docker network.
- **Ephemeral Storage**: All changes in the sandbox are lost once the container is destroyed.
- **TTL**: Containers are automatically cleaned up after a configurable time-to-live (default 30 minutes).
