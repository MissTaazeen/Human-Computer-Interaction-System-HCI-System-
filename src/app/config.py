# src/app/config.py

"""
Configuration module for Phase 1 of the Hand Gesture HCI project.

Only includes settings needed for:
- Webcam hand tracking
- Smooth cursor movement (no clicking yet)
"""


# Camera settings
CAMERA_INDEX: int = 0  # Default laptop webcam
FRAME_WIDTH: int | None = None  # e.g., 1280 or None to use default
FRAME_HEIGHT: int | None = None  # e.g., 720 or None to use default


# Hand tracking (MediaPipe Hands) settings
DETECTION_CONFIDENCE: float = 0.7
TRACKING_CONFIDENCE: float = 0.7
MAX_NUM_HANDS: int = 1

# Landmark indices (MediaPipe Hands)
INDEX_FINGER_TIP: int = 8  # Used for cursor control in Phase 1


# Cursor smoothing settings
# Smoothing factor for EMA:
# new = prev + (1 / SMOOTHING_FACTOR) * (target - prev)
SMOOTHING_FACTOR: float = 7.0


def get_smoothing_alpha() -> float:
    """
    Convert the integer-like SMOOTHING_FACTOR into an EMA alpha in (0, 1].

    Example:
        factor = 7  -> alpha ≈ 1 / 7 ≈ 0.14
    """
    return 1.0 / SMOOTHING_FACTOR
