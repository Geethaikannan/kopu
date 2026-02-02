# main.py
# Entry point for the PC Activity Monitoring Agent.
# This script runs the agent in the background, starting keyboard monitoring and periodic data sending.
# It ensures the agent continues running indefinitely without crashing on failures.

import threading
import time
from key_monitor import start_keyboard_monitoring, get_counters, reset_counters
from app_monitor import get_current_app_name
from risk import calculate_risk_score
from backend_sender import periodic_sender

# Configuration
USER_ID = "demo-user"  # Fixed user ID for this demo; in production, this could be dynamic

def main():
    """
    Main function to start the monitoring agent.
    """
    print("Starting PC Activity Monitoring Agent...")

    # Start keyboard monitoring in a background thread
    keyboard_listener = start_keyboard_monitoring()

    # Start periodic sender in a background thread
    sender_thread = threading.Thread(
        target=periodic_sender,
        args=(USER_ID, get_current_app_name, get_counters, calculate_risk_score, reset_counters),
        daemon=True
    )
    sender_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)  # Sleep to avoid busy waiting
    except KeyboardInterrupt:
        print("Stopping agent...")
        keyboard_listener.stop()

if __name__ == "__main__":
    main()
