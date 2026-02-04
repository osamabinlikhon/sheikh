from fastapi import APIRouter
from app.core.sandbox.manager import SandboxManager
from app.dependencies import get_sandbox_manager

router = APIRouter()

@router.get("/sandbox/{session_id}")
async def get_sandbox(session_id: str, sandbox_manager: SandboxManager = Depends(get_sandbox_manager)):
    return sandbox_manager.active_sandboxes.get(session_id)
