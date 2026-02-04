from fastapi import APIRouter
from app.core.sandbox.manager import SandboxManager
from app.dependencies import get_sandbox_manager

router = APIRouter()

@router.post("/sessions")
async def create_session(sandbox_manager: SandboxManager = Depends(get_sandbox_manager)):
    session = await sandbox_manager.create_sandbox("new_session")
    return session

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str, sandbox_manager: SandboxManager = Depends(get_sandbox_manager)):
    await sandbox_manager.destroy_sandbox(session_id)
    return {"status": "ok"}
