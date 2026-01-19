import os
import sys
import subprocess
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("App")

def build_frontend():
    """Builds the frontend if the dist directory is missing."""
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    dist_dir = os.path.join(frontend_dir, "dist")
    
    if not os.path.exists(dist_dir) or not os.path.exists(os.path.join(dist_dir, "index.html")):
        logger.info("Frontend build not found. Building frontend...")
        try:
            # Check if node_modules exists, if not install
            if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
                logger.info("Installing frontend dependencies...")
                subprocess.run("npm install", shell=True, cwd=frontend_dir, check=True)
            
            logger.info("Running npm build...")
            subprocess.run("npm run build", shell=True, cwd=frontend_dir, check=True)
            logger.info("Frontend built successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to build frontend: {e}")
            sys.exit(1)
    else:
        logger.info("Frontend build found. Skipping build.")

def run_server():
    """Starts the Uvicorn server."""
    # Add backend directory to sys.path so 'rag_core' can be imported by main.py
    backend_dir = os.path.join(os.getcwd(), "backend")
    sys.path.append(backend_dir)
    
    logger.info("Starting Backend Server at http://localhost:8000")
    
    # We run uvicorn programmatically
    # We use "backend.main:app" string so reload works if needed, 
    # but reload requires the import path to be resolvable.
    # Since we added backend to sys.path, "main:app" might work if we were in backend dir,
    # but we are in root. "backend.main:app" works if root is in path (it is).
    # BUT, inside main.py, "import rag_core" needs to work.
    # By adding backend_dir to sys.path, "import rag_core" usually works 
    # IF the module is loaded freely.
    
    try:
        uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
    except Exception as e:
        logger.error(f"Server error: {e}")

if __name__ == "__main__":
    print("===================================================")
    print("           Starting Mini RAG Application           ")
    print("===================================================")
    
    # 1. Ensure Frontend is built
    build_frontend()
    
    # 2. Run the Server
    run_server()
