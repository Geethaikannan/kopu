#!/usr/bin/env python3
"""
KOPU - PC Activity Monitoring & Alert System Launcher
This script starts all components of the KOPU system:
1. FastAPI Backend
2. PC Agent
3. Frontend (opens in browser)
"""

import subprocess
import sys
import os
import time
import webbrowser
import signal
import threading
from pathlib import Path

# Configuration
BACKEND_URL = "http://127.0.0.1:5000"
FRONTEND_URL = "http://127.0.0.1:5500/frontend/index.html"  # Live Server default
HEALTH_CHECK_RETRIES = 30
HEALTH_CHECK_INTERVAL = 1  # seconds

# Global processes
backend_process = None
agent_process = None
shutdown_requested = False


def print_header():
    """Print system header."""
    print("=" * 60)
    print("  KOPU - PC Activity Monitoring & Alert System")
    print("=" * 60)
    print()


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        sys.exit(1)


def install_requirements():
    """Install required packages."""
    print("📦 Checking dependencies...")
    
    # Backend requirements
    backend_req = Path("backend/requirements.txt")
    if backend_req.exists():
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-q", "-r", str(backend_req)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("  ✓ Backend dependencies installed")
        except subprocess.CalledProcessError:
            print("  ✗ Failed to install backend dependencies")
            return False
    
    # Agent requirements
    agent_req = Path("pc-agent/requirements.txt")
    if agent_req.exists():
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-q", "-r", str(agent_req)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("  ✓ Agent dependencies installed")
        except subprocess.CalledProcessError:
            print("  ✗ Failed to install agent dependencies")
            return False
    
    print()
    return True


def start_backend():
    """Start the FastAPI backend."""
    global backend_process
    
    print("🚀 Starting FastAPI Backend...")
    
    # Change to backend directory
    backend_dir = Path("backend")
    
    # Start backend process
    try:
        if os.name == 'nt':  # Windows
            backend_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "5000"],
                cwd=str(backend_dir),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:  # Unix/Linux/Mac
            backend_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "5000"],
                cwd=str(backend_dir),
                preexec_fn=os.setsid
            )
        
        print(f"  ✓ Backend process started (PID: {backend_process.pid})")
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to start backend: {e}")
        return False


def wait_for_backend():
    """Wait for backend to be ready."""
    print("⏳ Waiting for backend to be ready...")
    
    import urllib.request
    import urllib.error
    
    for i in range(HEALTH_CHECK_RETRIES):
        try:
            response = urllib.request.urlopen(
                f"{BACKEND_URL}/api/health", 
                timeout=2
            )
            if response.status == 200:
                print("  ✓ Backend is ready!")
                print()
                return True
        except urllib.error.URLError:
            pass
        except Exception:
            pass
        
        time.sleep(HEALTH_CHECK_INTERVAL)
        print(f"  ... retrying ({i+1}/{HEALTH_CHECK_RETRIES})")
    
    print("  ✗ Backend failed to start within timeout")
    return False


def start_agent():
    """Start the PC Agent."""
    global agent_process
    
    print("🖥️  Starting PC Agent...")
    
    agent_dir = Path("pc-agent")
    
    try:
        # Use start_agent.py for better handling
        if os.name == 'nt':  # Windows
            agent_process = subprocess.Popen(
                [sys.executable, "start_agent.py"],
                cwd=str(agent_dir),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:  # Unix/Linux/Mac
            agent_process = subprocess.Popen(
                [sys.executable, "start_agent.py"],
                cwd=str(agent_dir),
                preexec_fn=os.setsid
            )
        
        print(f"  ✓ Agent process started (PID: {agent_process.pid})")
        print()
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to start agent: {e}")
        return False


def open_frontend():
    """Open frontend in browser."""
    print("🌐 Opening Dashboard in browser...")
    
    # Try to find the frontend
    frontend_paths = [
        Path("frontend/index.html"),
        Path("index.html"),
    ]
    
    frontend_path = None
    for path in frontend_paths:
        if path.exists():
            frontend_path = path.absolute()
            break
    
    if frontend_path:
        # Open with file protocol (simplest for local use)
        url = f"file://{frontend_path}"
        webbrowser.open(url)
        print(f"  ✓ Opened: {url}")
        print()
    else:
        print("  ⚠ Frontend not found. Please open frontend/index.html manually")
        print()


def print_status():
    """Print system status."""
    print("=" * 60)
    print("  System Status")
    print("=" * 60)
    print(f"  Backend:  {BACKEND_URL}")
    print(f"  API Docs: {BACKEND_URL}/docs")
    print(f"  Health:   {BACKEND_URL}/api/health")
    print()
    print("  Default Login:")
    print("    Username: admin")
    print("    Password: admin123")
    print()
    print("  Press Ctrl+C to stop all services")
    print("=" * 60)
    print()


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    global shutdown_requested
    shutdown_requested = True
    print("\n\n🛑 Shutdown requested...")
    shutdown()


def shutdown():
    """Shutdown all processes gracefully."""
    global backend_process, agent_process
    
    print("🧹 Cleaning up...")
    
    # Terminate agent
    if agent_process:
        print("  Stopping agent...")
        try:
            if os.name == 'nt':  # Windows
                agent_process.terminate()
            else:
                os.killpg(os.getpgid(agent_process.pid), signal.SIGTERM)
            agent_process.wait(timeout=5)
        except:
            try:
                agent_process.kill()
            except:
                pass
    
    # Terminate backend
    if backend_process:
        print("  Stopping backend...")
        try:
            if os.name == 'nt':  # Windows
                backend_process.terminate()
            else:
                os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
            backend_process.wait(timeout=5)
        except:
            try:
                backend_process.kill()
            except:
                pass
    
    print("  ✓ All services stopped")
    print("\n👋 Goodbye!")
    sys.exit(0)


def monitor_processes():
    """Monitor processes and restart if needed."""
    global backend_process, agent_process, shutdown_requested
    
    while not shutdown_requested:
        # Check backend
        if backend_process and backend_process.poll() is not None:
            print("⚠ Backend process died, restarting...")
            start_backend()
        
        # Check agent
        if agent_process and agent_process.poll() is not None:
            print("⚠ Agent process died, restarting...")
            start_agent()
        
        time.sleep(5)


def main():
    """Main entry point."""
    global shutdown_requested
    
    print_header()
    check_python_version()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    if os.name != 'nt':
        signal.signal(signal.SIGHUP, signal_handler)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Start backend
    if not start_backend():
        print("❌ Failed to start backend")
        sys.exit(1)
    
    # Wait for backend
    if not wait_for_backend():
        shutdown()
        sys.exit(1)
    
    # Start agent
    if not start_agent():
        print("⚠ Agent failed to start, continuing without agent...")
    
    # Open frontend
    open_frontend()
    
    # Print status
    print_status()
    
    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_processes, daemon=True)
    monitor_thread.start()
    
    # Keep main thread alive
    try:
        while not shutdown_requested:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":
    main()
