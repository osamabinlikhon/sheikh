from fastapi import APIRouter, Depends, WebSocket
from starlette.websockets import WebSocketDisconnect
from app.core.agent.planact import PlanActAgent
from app.dependencies import get_agent

router = APIRouter()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, agent: PlanActAgent = Depends(get_agent)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            async for response in agent.run(data, session_id):
                await websocket.send_json(response)
    except WebSocketDisconnect:
        pass
