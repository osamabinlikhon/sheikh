from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, Optional
import subprocess
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sandbox API",
    description="API for sandbox container operations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    command: str
    cwd: Optional[str] = None
    timeout: Optional[int] = 30

class FileRequest(BaseModel):
    path: str
    content: Optional[str] = None
    recursive: Optional[bool] = False

@app.get("/")
async def root():
    return {"message": "Sandbox API is running", "session_id": os.environ.get("SESSION_ID", "unknown")}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "session_id": os.environ.get("SESSION_ID", "unknown")}

@app.post("/api/terminal/command")
async def execute_command(request: CommandRequest):
    """Execute a command in the sandbox."""
    try:
        # Set working directory if provided
        cwd = request.cwd or "/workspace"
        
        # Ensure working directory exists
        os.makedirs(cwd, exist_ok=True)
        
        # Execute command
        result = subprocess.run(
            request.command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=request.timeout
        )
        
        return {
            "success": True,
            "command": request.command,
            "cwd": cwd,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command timed out")
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/list")
async def list_files(path: str = "/workspace", recursive: bool = False):
    """List files in a directory."""
    try:
        abs_path = os.path.abspath(path)
        
        # Security check: ensure path is within workspace
        if not abs_path.startswith("/workspace"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail="Path not found")
        
        if not os.path.isdir(abs_path):
            raise HTTPException(status_code=400, detail="Path is not a directory")
        
        files = []
        directories = []
        
        if recursive:
            for root, dirs, filenames in os.walk(abs_path):
                rel_root = os.path.relpath(root, abs_path)
                if rel_root == ".":
                    rel_root = ""
                
                for d in dirs:
                    directories.append(os.path.join(rel_root, d))
                
                for f in filenames:
                    files.append(os.path.join(rel_root, f))
        else:
            for item in os.listdir(abs_path):
                item_path = os.path.join(abs_path, item)
                if os.path.isfile(item_path):
                    files.append(item)
                elif os.path.isdir(item_path):
                    directories.append(item)
        
        return {
            "success": True,
            "path": abs_path,
            "files": sorted(files),
            "directories": sorted(directories),
            "total_files": len(files),
            "total_directories": len(directories)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"List files failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/read")
async def read_file(path: str):
    """Read a file."""
    try:
        abs_path = os.path.abspath(path)
        
        # Security check: ensure path is within workspace
        if not abs_path.startswith("/workspace"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        if not os.path.isfile(abs_path):
            raise HTTPException(status_code=400, detail="Path is not a file")
        
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "path": abs_path,
            "content": content,
            "size": len(content)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Read file failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/files/write")
async def write_file(request: FileRequest):
    """Write to a file."""
    try:
        abs_path = os.path.abspath(request.path)
        
        # Security check: ensure path is within workspace
        if not abs_path.startswith("/workspace"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not request.content:
            raise HTTPException(status_code=400, detail="Content is required")
        
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(request.content)
        
        return {
            "success": True,
            "path": abs_path,
            "size": len(request.content)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Write file failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/files/delete")
async def delete_file(path: str, recursive: bool = False):
    """Delete a file or directory."""
    try:
        abs_path = os.path.abspath(path)
        
        # Security check: ensure path is within workspace
        if not abs_path.startswith("/workspace"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail="File or directory not found")
        
        if os.path.isfile(abs_path):
            os.remove(abs_path)
            return {
                "success": True,
                "path": abs_path,
                "type": "file"
            }
        elif os.path.isdir(abs_path):
            if recursive:
                import shutil
                shutil.rmtree(abs_path)
            else:
                os.rmdir(abs_path)
            
            return {
                "success": True,
                "path": abs_path,
                "type": "directory",
                "recursive": recursive
            }
        else:
            raise HTTPException(status_code=400, detail="Unknown file type")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete file failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/files/mkdir")
async def create_directory(request: FileRequest):
    """Create a directory."""
    try:
        abs_path = os.path.abspath(request.path)
        
        # Security check: ensure path is within workspace
        if not abs_path.startswith("/workspace"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        os.makedirs(abs_path, exist_ok=True, mode=0o755)
        
        return {
            "success": True,
            "path": abs_path,
            "recursive": request.recursive
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create directory failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/exists")
async def check_exists(path: str):
    """Check if file or directory exists."""
    try:
        abs_path = os.path.abspath(path)
        
        # Security check: ensure path is within workspace
        if not abs_path.startswith("/workspace"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        exists = os.path.exists(abs_path)
        file_type = "file" if os.path.isfile(abs_path) else "directory" if os.path.isdir(abs_path) else "unknown"
        
        return {
            "success": True,
            "path": abs_path,
            "exists": exists,
            "type": file_type
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Check exists failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/browser/status")
async def browser_status():
    """Check browser status."""
    try:
        # Check if Chrome is running
        result = subprocess.run(
            "pgrep -f chrome",
            shell=True,
            capture_output=True,
            text=True
        )
        
        chrome_running = result.returncode == 0
        
        # Check if remote debugging port is open
        debug_port_result = subprocess.run(
            "netstat -tlnp | grep 9222",
            shell=True,
            capture_output=True,
            text=True
        )
        
        debug_port_open = debug_port_result.returncode == 0
        
        return {
            "success": True,
            "chrome_running": chrome_running,
            "debug_port_open": debug_port_open,
            "debug_port": 9222
        }
        
    except Exception as e:
        logger.error(f"Browser status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=False
    )