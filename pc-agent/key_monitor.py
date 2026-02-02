# key_monitor.py
# This module monitors keyboard activity using pynput.
# It counts keystrokes and detects suspicious keywords without storing raw text.
# Keywords are checked in a temporary buffer that is cleared immediately after detection.
# This ensures privacy by not persisting any raw keystroke data.

from pynput import keyboard
import threading
from keywords import SUSPICIOUS_KEYWORDS

# Global counters (thread-safe with locks if needed, but for simplicity, assuming single-threaded access)
total_keystrokes = 0
suspicious_count = 0
current_word = ""  # Temporary buffer for word building, cleared after space or keyword check

def on_press(key):
    global total_keystrokes, suspicious_count, current_word
    total_keystrokes += 1

    try:
        # Get the character from the key
        char = key.char if hasattr(key, 'char') and key.char else ''
        if char.isalnum() or char == ' ':
            if char == ' ':
                # Check for keyword when space is pressed
                if current_word.lower() in SUSPICIOUS_KEYWORDS:
                    suspicious_count += 1
                current_word = ""
            else:
                current_word += char
        elif key == keyboard.Key.space:
            # Handle space key
            if current_word.lower() in SUSPICIOUS_KEYWORDS:
                suspicious_count += 1
            current_word = ""
        elif key == keyboard.Key.enter:
            # Handle enter key
            if current_word.lower() in SUSPICIOUS_KEYWORDS:
                suspicious_count += 1
            current_word = ""
    except AttributeError:
        # Special keys like shift, ctrl, etc., ignore for word building
        pass

def start_keyboard_monitoring():
    """
    Start the keyboard listener in a background thread.
    """
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return listener

def get_counters():
    """
    Get the current counters for keystrokes and suspicious detections.

    Returns:
        tuple: (total_keystrokes, suspicious_count)
    """
    return total_keystrokes, suspicious_count

def reset_counters():
    """
    Reset the counters after sending data.
    """
    global total_keystrokes, suspicious_count, current_word
    total_keystrokes = 0
    suspicious_count = 0
    current_word = ""
