import json
from pathlib import Path

SETTINGS_FILE = Path("src/app/settings.json")


def load_settings() -> dict:
    """Load gesture settings from JSON."""
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)

    return {
        "pinch_threshold": 40,
        "click_hold_frames": 3,
        "drag_hold_frames": 8,
        "smoothing_factor": 12,
        "enable_clicks": True,
    }


def save_settings(data: dict) -> None:
    """Save updated settings back to JSON."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)
