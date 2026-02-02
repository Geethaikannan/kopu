# app_monitor.py
# This module monitors the currently running application using psutil.
# It identifies the application name by finding the process with the highest CPU usage.
# This is a proxy for the active application, as direct active window detection requires additional libraries.
# Handles permission errors gracefully.

import psutil

def get_current_app_name():
    """
    Get the name of the currently active application.

    Returns:
        str: Name of the application, or "Unknown" if unable to determine.
    """
    try:
        # Get all processes
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not processes:
            return "Unknown"

        # Find the process with the highest CPU usage (proxy for active app)
        active_proc = max(processes, key=lambda p: p['cpu_percent'] or 0)
        return active_proc['name'] or "Unknown"
    except Exception as e:
        print(f"Error getting current app name: {e}")
        return "Unknown"
