# -----------------------------
# Camera settings
# -----------------------------
CAMERA_INDEX: int = 0
FRAME_WIDTH: int | None = None
FRAME_HEIGHT: int | None = None

# -----------------------------
# MediaPipe Hand Tracking
# -----------------------------
DETECTION_CONFIDENCE: float = 0.7
TRACKING_CONFIDENCE: float = 0.7
MAX_NUM_HANDS: int = 1

# -----------------------------
# Landmark index
# -----------------------------
INDEX_FINGER_TIP: int = 8

# -----------------------------
# Cursor smoothing + control
# -----------------------------
SMOOTHING_FACTOR = 22.0         # Higher = smoother, slower
CURSOR_SPEED = 0.25             # 0.2 slow, 0.5 medium, 1.0 instant
HAND_LOST_FREEZE = True         # Freeze cursor when hand disappears
REACQUIRE_DELAY = 6             # Frames before allowing movement again

# Cursor stability (prevents drift)
MOVEMENT_DEADZONE_PX = 8        # Increase if cursor still drifts


# -----------------------------
# Pinch click settings
# -----------------------------
PINCH_THRESHOLD: int = 40
CLICK_COOLDOWN_FRAMES: int = 15

# -----------------------------
# Safety toggle
# -----------------------------
ENABLE_CLICKS: bool = True


def get_smoothing_alpha() -> float:
    """
    Convert smoothing factor into EMA alpha.
    Smaller alpha = smoother but more lag.
    """
    return 1.0 / SMOOTHING_FACTOR
