import docker
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
from loguru import logger

from app.config import settings
from app.core.sandbox.docker_client import DockerClient


class SandboxManager:
    """Manages Docker sandbox containers for isolated execution."""
    
    def __init__(
        self,
        docker_client: DockerClient,
        image: str = None,
        network: str = None,
        ttl_minutes: int = None
    ):
        self.docker = docker_client
        self.image = image or settings.sandbox_image
        self.network = network or settings.sandbox_network
        self.ttl = timedelta(minutes=ttl_minutes or settings.sandbox_ttl_minutes)
        self.active_sandboxes: Dict[str, Dict] = {}
    
    async def create_sandbox(self, session_id: str) -> Dict:
        """Create a new sandbox container for a session."""
        
        container_name = f"{settings.sandbox_name_prefix}-{session_id}"
        
        try:
            # Create container
            container = await self.docker.create_container(
                image=self.image,
                name=container_name,
                environment={
                    "SESSION_ID": session_id,
                    "DISPLAY": ":99"
                },
                network=self.network,
                cap_add=["SYS_ADMIN"],  # For Chrome
                shm_size="2g",  # Shared memory for Chrome
                mem_limit="2g",
                cpu_period=100000,
                cpu_quota=150000,  # 1.5 CPU cores
                ports={
                    8080: None,  # API port
                    5900: None,  # VNC port
                    6080: None   # WebSocket VNC port
                }
            )
            
            # Start container
            await self.docker.start_container(container.id)
            
            # Wait for services to start
            await self._wait_for_services(container)
            
            # Get container details
            container_info = await self._get_container_info(container)
            
            # Register sandbox
            self.active_sandboxes[session_id] = {
                "container": container,
                "container_id": container.id,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + self.ttl,
                "container_info": container_info
            }
            
            logger.info(f"Created sandbox for session {session_id}")
            
            return {
                "session_id": session_id,
                "container_id": container.id,
                "status": "ready",
                "container_info": container_info
            }
            
        except Exception as e:
            logger.error(f"Failed to create sandbox for session {session_id}: {e}")
            raise
    
    async def destroy_sandbox(self, session_id: str) -> None:
        """Destroy a sandbox container."""
        
        if session_id not in self.active_sandboxes:
            logger.warning(f"Sandbox for session {session_id} not found")
            return
        
        sandbox_info = self.active_sandboxes[session_id]
        container_id = sandbox_info["container_id"]
        
        try:
            # Stop container
            await self.docker.stop_container(container_id, timeout=10)
            
            # Remove container
            await self.docker.remove_container(container_id, force=True)
            
            # Remove from active sandboxes
            del self.active_sandboxes[session_id]
            
            logger.info(f"Destroyed sandbox for session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to destroy sandbox for session {session_id}: {e}")
            raise
    
    async def get_sandbox(self, session_id: str) -> Optional[Dict]:
        """Get sandbox information for a session."""
        
        if session_id not in self.active_sandboxes:
            return None
        
        sandbox_info = self.active_sandboxes[session_id]
        
        # Check if sandbox has expired
        if datetime.utcnow() > sandbox_info["expires_at"]:
            await self.destroy_sandbox(session_id)
            return None
        
        return sandbox_info
    
    async def list_sandboxes(self) -> List[Dict]:
        """List all active sandboxes."""
        
        sandboxes = []
        expired_sessions = []
        
        for session_id, sandbox_info in self.active_sandboxes.items():
            # Check if sandbox has expired
            if datetime.utcnow() > sandbox_info["expires_at"]:
                expired_sessions.append(session_id)
            else:
                sandboxes.append({
                    "session_id": session_id,
                    "container_id": sandbox_info["container_id"],
                    "created_at": sandbox_info["created_at"],
                    "expires_at": sandbox_info["expires_at"],
                    "container_info": sandbox_info["container_info"]
                })
        
        # Clean up expired sandboxes
        for session_id in expired_sessions:
            await self.destroy_sandbox(session_id)
        
        return sandboxes
    
    async def cleanup_expired_sandboxes(self) -> None:
        """Remove expired sandbox containers."""
        
        expired_sessions = []
        
        for session_id, sandbox_info in self.active_sandboxes.items():
            if datetime.utcnow() > sandbox_info["expires_at"]:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            await self.destroy_sandbox(session_id)
    
    async def execute_command(
        self,
        session_id: str,
        command: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute a command in a sandbox container."""
        
        sandbox_info = await self.get_sandbox(session_id)
        if not sandbox_info:
            raise ValueError(f"Sandbox for session {session_id} not found or expired")
        
        container_id = sandbox_info["container_id"]
        return await self.docker.execute_command(container_id, command, **kwargs)
    
    async def get_container_logs(
        self,
        session_id: str,
        **kwargs
    ) -> str:
        """Get logs from a sandbox container."""
        
        sandbox_info = await self.get_sandbox(session_id)
        if not sandbox_info:
            raise ValueError(f"Sandbox for session {session_id} not found or expired")
        
        container_id = sandbox_info["container_id"]
        return await self.docker.get_container_logs(container_id, **kwargs)
    
    async def _wait_for_services(self, container) -> None:
        """Wait for sandbox services to start."""
        
        # Wait for container to be ready
        import time
        max_wait = 60  # 60 seconds max wait
        wait_time = 0
        
        while wait_time < max_wait:
            try:
                # Try to execute a simple command to check if container is ready
                result = await self.docker.execute_command(
                    container.id,
                    "echo 'ready'",
                    stdout=True,
                    stderr=True
                )
                
                if result["exit_code"] == 0:
                    break
                    
            except Exception as e:
                logger.debug(f"Waiting for container {container.id} to be ready: {e}")
                time.sleep(1)
                wait_time += 1
        
        if wait_time >= max_wait:
            raise TimeoutError(f"Container {container.id} did not become ready within {max_wait} seconds")
    
    async def _get_container_info(self, container) -> Dict[str, Any]:
        """Get container information."""
        
        try:
            container.reload()
            
            # Get port mappings
            ports = container.ports
            
            return {
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "ports": ports,
                "created": container.attrs["Created"],
                "image": container.image.tags[0] if container.image.tags else container.image.id
            }
            
        except Exception as e:
            logger.error(f"Failed to get container info for {container.id}: {e}")
            return {
                "id": container.id,
                "name": container.name,
                "status": "unknown",
                "ports": {},
                "created": None,
                "image": None
            }