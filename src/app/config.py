# Camera settings
CAMERA_INDEX: int = 0
FRAME_WIDTH: int | None = None
FRAME_HEIGHT: int | None = None


# MediaPipe Hand Tracking
DETECTION_CONFIDENCE: float = 0.7
TRACKING_CONFIDENCE: float = 0.7
MAX_NUM_HANDS: int = 1


# Landmark index
INDEX_FINGER_TIP: int = 8


# Cursor smoothing
SMOOTHING_FACTOR = 15.0
REACQUIRE_DELAY = 6

# Pinch click settings
PINCH_THRESHOLD: int = 40
CLICK_COOLDOWN_FRAMES: int = 15

# Safety toggle
ENABLE_CLICKS: bool = True


def get_smoothing_alpha() -> float:
    return 1.0 / SMOOTHING_FACTOR
