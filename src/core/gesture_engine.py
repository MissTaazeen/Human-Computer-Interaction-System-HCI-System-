import cv2

from core.camera import Camera
from core.hand_tracker import HandTracker
from core.cursor_mapper import CursorMapper
from core.smoothing import Smoother
from core.gesture_recognizer import GestureRecognizer
from core.actions import ActionController

from app import config


class GestureEngine:
    """
    Phase 4 Gesture Engine (GUI Mode)

    Runs:
    Camera → Hand Tracking → Cursor Movement → Click

    IMPORTANT:
    - No cv2.imshow()
    - Frames stored in latest_frame for GUI
    """

    def __init__(self):
        self.running = False

        # -----------------------------
        # Core Components
        # -----------------------------
        self.camera = Camera(
            device_index=config.CAMERA_INDEX,
            frame_width=config.FRAME_WIDTH,
            frame_height=config.FRAME_HEIGHT,
        )

        self.tracker = HandTracker(
            max_num_hands=config.MAX_NUM_HANDS,
            detection_confidence=config.DETECTION_CONFIDENCE,
            tracking_confidence=config.TRACKING_CONFIDENCE,
        )

        self.smoother = Smoother(alpha=config.get_smoothing_alpha())
        self.mapper = CursorMapper(self.smoother)

        self.recognizer = GestureRecognizer(
            pinch_threshold=config.PINCH_THRESHOLD
        )

        self.actions = ActionController()

        # -----------------------------
        # GUI Runtime Settings
        # -----------------------------
        self.enable_clicks = True

        # Latest Frame for GUI Display
        self.latest_frame = None

    # -----------------------------
    # Main Loop (Thread)
    # -----------------------------
    def start(self):
        """Runs gesture controller loop inside QThread"""
        self.running = True

        while self.running:
            frame = self.camera.get_frame()
            if frame is None:
                continue

            annotated, landmarks = self.tracker.detect(frame, draw=True)

            # -----------------------------
            # Cursor Movement
            # -----------------------------
            if landmarks:
                index_points = [
                    lm for lm in landmarks
                    if lm[0] == config.INDEX_FINGER_TIP
                ]

                if index_points:
                    _, x, y = index_points[0]
                    h, w, _ = annotated.shape

                    self.mapper.move_cursor(
                        x_frame=x,
                        y_frame=y,
                        frame_width=w,
                        frame_height=h,
                    )

            # -----------------------------
            # Click Detection
            # -----------------------------
            if landmarks:
                if self.recognizer.detect_click_event(landmarks):
                    if self.enable_clicks:
                        self.actions.left_click()

            # -----------------------------
            # Store Frame for GUI
            # -----------------------------
            self.latest_frame = annotated.copy()

    # -----------------------------
    # Stop Engine Safely
    # -----------------------------
    def stop(self):
        """Stops gesture loop and releases resources"""
        self.running = False

        self.camera.release()
        self.tracker.close()
