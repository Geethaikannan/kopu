# backend_sender.py
# This module handles sending activity metadata to the backend server.
# It sends data every 30 seconds via POST request to the specified endpoint.
# Uses only metadata (no raw data) to ensure privacy.
# Includes retry logic - if backend is down, retries every 5 seconds.
# Failures are logged but do not crash the agent.

import requests
import time

BACKEND_URL = "http://127.0.0.1:5000/api/activity/log"
API_KEY = "kopu-agent-key-001"
SEND_INTERVAL = 30  # seconds
RETRY_INTERVAL = 5  # seconds when backend is down

def send_activity_data(user_id, app_name, risk_score):
    """
    Send activity data to the backend.

    Args:
        user_id (str): User identifier.
        app_name (str): Name of the current application.
        risk_score (float): Calculated risk score.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    payload = {
        "userId": user_id,
        "appName": app_name,
        "eventType": "KEYWORD",
        "riskScore": risk_score
    }
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(BACKEND_URL, json=payload, headers=headers, timeout=5)
        if response.status_code == 201:
            print(f"Activity data sent successfully. Risk: {risk_score}")
            return True
        else:
            print(f"Failed to send data: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Error sending data to backend: {e}")
        return False

def wait_for_backend():
    """
    Wait until backend is available.
    Retries every 5 seconds.
    """
    print("Waiting for backend to be available...")
    while True:
        try:
            response = requests.get("http://127.0.0.1:5000/api/health", timeout=2)
            if response.status_code == 200:
                print("Backend is available!")
                return True
        except requests.RequestException:
            pass
        print(f"Backend not available, retrying in {RETRY_INTERVAL} seconds...")
        time.sleep(RETRY_INTERVAL)

def periodic_sender(user_id, get_app_name_func, get_counters_func, calculate_risk_func, reset_counters_func):
    """
    Run a loop to send data every 30 seconds.
    If backend is down, retries every 5 seconds without crashing.

    Args:
        user_id (str): User identifier.
        get_app_name_func (callable): Function to get current app name.
        get_counters_func (callable): Function to get counters.
        calculate_risk_func (callable): Function to calculate risk score.
        reset_counters_func (callable): Function to reset counters.
    """
    # Wait for backend to be available before starting
    wait_for_backend()
    
    while True:
        time.sleep(SEND_INTERVAL)
        app_name = get_app_name_func()
        total_keystrokes, suspicious_count = get_counters_func()
        risk_score = calculate_risk_func(suspicious_count, total_keystrokes)
        
        success = send_activity_data(user_id, app_name, risk_score)
        
        if success:
            reset_counters_func()
        else:
            # If send failed, don't reset counters - try again next cycle
            # The counters will accumulate until successfully sent
            print("Will retry sending data in next cycle...")
