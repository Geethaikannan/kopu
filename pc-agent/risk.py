# risk.py
# This module contains the risk scoring logic for the PC Activity Monitoring Agent.
# The risk score is calculated based on suspicious keyword detections relative to total keystrokes.
# This approach ensures privacy by using only counters, not raw data.

def calculate_risk_score(suspicious_count, total_keystrokes):
    """
    Calculate the risk score based on suspicious keyword detections.

    Args:
        suspicious_count (int): Number of suspicious keywords detected.
        total_keystrokes (int): Total number of keystrokes recorded.

    Returns:
        float: Risk score rounded to 2 decimal places. Returns 0.0 if total_keystrokes is 0.
    """
    if total_keystrokes == 0:
        return 0.0
    risk = (suspicious_count / total_keystrokes) * 10
    return round(risk, 2)
