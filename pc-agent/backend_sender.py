# backend_sender.py
# This module handles sending activity metadata to the backend server.
# It sends data every 60 seconds via POST request to the specified endpoint.
# Uses only metadata (no raw data) to ensure privacy.
# Failures are logged but do not crash the agent.

import requests
import time

BACKEND_URL = "http://localhost:5000/api/activity/log"

def send_activity_data(user_id, app_name, risk_score):
    """
    Send activity data to the backend.

    Args:
        user_id (str): User identifier.
        app_name (str): Name of the current application.
        risk_score (float): Calculated risk score.
    """
    payload = {
        "userId": user_id,
        "appName": app_name,
        "eventType": "KEYWORD",
        "riskScore": risk_score
    }
    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=5)
        if response.status_code == 201:
            print("Activity data sent successfully.")
        else:
            print(f"Failed to send data: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"Error sending data to backend: {e}")

def periodic_sender(user_id, get_app_name_func, get_counters_func, calculate_risk_func, reset_counters_func):
    """
    Run a loop to send data every 60 seconds.

    Args:
        user_id (str): User identifier.
        get_app_name_func (callable): Function to get current app name.
        get_counters_func (callable): Function to get counters.
        calculate_risk_func (callable): Function to calculate risk score.
        reset_counters_func (callable): Function to reset counters.
    """
    while True:
        time.sleep(60)
        app_name = get_app_name_func()
        total_keystrokes, suspicious_count = get_counters_func()
        risk_score = calculate_risk_func(suspicious_count, total_keystrokes)
        send_activity_data(user_id, app_name, risk_score)
        reset_counters_func()
