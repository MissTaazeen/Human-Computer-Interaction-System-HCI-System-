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
SMOOTHING_FACTOR: float = 12.0

PINCH_THRESHOLD = 40
CLICK_COOLDOWN_FRAMES = 15

ENABLE_CLICKS = False

def get_smoothing_alpha() -> float:
    """
    Convert the integer-like SMOOTHING_FACTOR into an EMA alpha in (0, 1].
    """
    return 1.0 / SMOOTHING_FACTOR
