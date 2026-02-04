from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from loguru import logger

from app.config import settings
from app.api.v1 import auth, chat, sessions, tools, sandbox
from app.core.sandbox.manager import SandboxManager
from app.core.llm.codestral import CodestralClient
from app.core.tools.registry import ToolRegistry
from app.core.agent.planact import PlanActAgent
from app.core.sandbox.docker_client import DockerClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info("Starting Agent Sheikh Backend...")
    
    # Initialize core services
    app.state.docker_client = DockerClient()
    app.state.sandbox_manager = SandboxManager(
        docker_client=app.state.docker_client,
        network=settings.sandbox_network,
        ttl_minutes=settings.sandbox_ttl_minutes
    )
    
    app.state.llm_client = CodestralClient(
        api_key=settings.api_key,
        base_url=settings.api_base,
        model=settings.model_name
    )
    
    app.state.tool_registry = ToolRegistry()
    app.state.agent = PlanActAgent(
        llm_client=app.state.llm_client,
        tool_registry=app.state.tool_registry,
        max_iterations=settings.max_agent_iterations
    )
    
    logger.info("Agent Sheikh Backend started successfully")
    yield
    
    # Shutdown
    logger.info("Shutting down Agent Sheikh Backend...")
    await app.state.sandbox_manager.cleanup_expired_sandboxes()
    logger.info("Agent Sheikh Backend shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Agent Sheikh API",
        description="General-purpose AI Agent system with sandbox execution",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Include API routers
    app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
    app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
    app.include_router(sessions.router, prefix="/api/v1", tags=["Sessions"])
    app.include_router(tools.router, prefix="/api/v1", tags=["Tools"])
    app.include_router(sandbox.router, prefix="/api/v1", tags=["Sandbox"])
    
    @app.get("/")
    async def root():
        return {"message": "Agent Sheikh Backend is running"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": "1.0.0"}
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )