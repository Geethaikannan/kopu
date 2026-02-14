# main.py
# Entry point for the PC Activity Monitoring Agent.
# This script runs the agent in the background, starting keyboard monitoring and periodic data sending.
# It ensures the agent continues running indefinitely without crashing on failures.

import threading
import time
import logging
import sys
from key_monitor import start_keyboard_monitoring, get_counters, reset_counters
from app_monitor import get_current_app_name
from risk import calculate_risk_score
from backend_sender import periodic_sender

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration
USER_ID = "demo-user"  # Fixed user ID for this demo; in production, this could be dynamic

def main():
    """
    Main function to start the monitoring agent.
    Runs silently in background with proper error handling.
    """
    logger.info("=" * 50)
    logger.info("KOPU PC Activity Monitoring Agent")
    logger.info("=" * 50)
    logger.info("Starting agent...")

    try:
        # Start keyboard monitoring in a background thread
        logger.info("Starting keyboard monitoring...")
        keyboard_listener = start_keyboard_monitoring()
        logger.info("Keyboard monitoring started successfully")
    except Exception as e:
        logger.error(f"Failed to start keyboard monitoring: {e}")
        logger.info("Agent will continue without keyboard monitoring")
        keyboard_listener = None

    # Start periodic sender in a background thread
    logger.info("Starting data sender (will wait for backend)...")
    sender_thread = threading.Thread(
        target=periodic_sender,
        args=(USER_ID, get_current_app_name, get_counters, calculate_risk_score, reset_counters),
        daemon=True,
        name="DataSender"
    )
    sender_thread.start()
    logger.info("Data sender thread started")

    # Keep the main thread alive
    logger.info("Agent is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)  # Sleep to avoid busy waiting
    except KeyboardInterrupt:
        logger.info("Shutdown signal received...")
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}")
    finally:
        logger.info("Stopping agent...")
        if keyboard_listener:
            try:
                keyboard_listener.stop()
                logger.info("Keyboard monitoring stopped")
            except Exception as e:
                logger.error(f"Error stopping keyboard listener: {e}")
        logger.info("Agent stopped")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        sys.exit(1)
