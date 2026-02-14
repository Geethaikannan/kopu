#!/usr/bin/env python3
"""
KOPU PC Activity Monitoring Agent - Background Launcher
This script launches the agent as a background process with proper logging.
"""

import subprocess
import sys
import os
import platform
import argparse


def install_requirements():
    """Install required packages if not already installed."""
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    flag_file = os.path.join(os.path.dirname(__file__), "requirements_installed.txt")
    
    if os.path.exists(flag_file):
        return True
    
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        with open(flag_file, "w") as f:
            f.write("installed")
        print("Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        return False


def run_agent_foreground():
    """Run the agent in foreground mode."""
    from main import main
    main()


def run_agent_background():
    """Run the agent in background mode (Windows)."""
    if platform.system() != "Windows":
        print("Background mode is only supported on Windows")
        print("Running in foreground mode instead...")
        run_agent_foreground()
        return
    
    # Create a detached process on Windows
    import subprocess
    import ctypes
    
    # Hide the console window
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    # Run the agent
    run_agent_foreground()


def main():
    parser = argparse.ArgumentParser(description="KOPU PC Activity Monitoring Agent Launcher")
    parser.add_argument(
        "--background", "-b",
        action="store_true",
        help="Run in background mode (Windows only)"
    )
    parser.add_argument(
        "--install", "-i",
        action="store_true",
        help="Install requirements and exit"
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("KOPU PC Activity Monitoring Agent Launcher")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        sys.exit(1)
    
    # Install requirements if needed
    if not install_requirements():
        sys.exit(1)
    
    if args.install:
        print("Requirements installed. Exiting.")
        sys.exit(0)
    
    # Run the agent
    if args.background:
        print("Starting agent in background mode...")
        run_agent_background()
    else:
        print("Starting agent in foreground mode...")
        print("Press Ctrl+C to stop")
        print("-" * 50)
        run_agent_foreground()


if __name__ == "__main__":
    main()
