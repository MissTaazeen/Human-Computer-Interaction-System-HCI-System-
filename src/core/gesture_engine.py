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

    Pipeline:
    Camera → Hand Tracking → Cursor Move → Click/Drag Actions

    Features:
    - No cv2.imshow()
    - Frames stored for GUI display
    - Cursor freezes when hand is lost
    - Click + Drag fully supported
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

        # Smoother + Cursor Mapper
        self.smoother = Smoother(alpha=config.get_smoothing_alpha())
        self.mapper = CursorMapper(self.smoother)

        # Gesture Recognition
        self.recognizer = GestureRecognizer(
            pinch_threshold=config.PINCH_THRESHOLD
        )

        # Mouse Actions
        self.actions = ActionController()

        # GUI Frame Output
        self.latest_frame = None

        # Toggle Clicks
        self.enable_clicks = config.ENABLE_CLICKS
        self.enable_drag = True

    # -----------------------------
    # Start Engine Loop
    # -----------------------------
    def start(self):
        """Main gesture loop (runs inside QThread)."""
        self.running = True
        print("Gesture Engine Started...")

        while self.running:
            frame = self.camera.get_frame()
            if frame is None:
                continue

            annotated, landmarks = self.tracker.detect(frame, draw=True)

            # -----------------------------
            # Cursor Movement
            # -----------------------------
            if landmarks:
                self.mapper.resume()

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

            else:
                # Hand lost → freeze cursor + stop drag
                self.mapper.freeze()
                self.actions.stop_drag()
                self.recognizer.reset_state()

            # -----------------------------
            # Gesture Actions (Click + Drag)
            # -----------------------------
            if landmarks:
                # Update drag state every frame
                self.recognizer.update_drag_state(landmarks)

                # ---- DRAG MODE ----
                if self.recognizer.is_dragging() and self.enable_drag:
                    self.actions.start_drag()
                else:
                    self.actions.stop_drag()


                else:
                    # Release mouse if not dragging
                    self.actions.stop_drag()

                    # Click ONLY when not dragging
                    if self.recognizer.detect_click_event(landmarks):
                        if self.enable_clicks:
                            self.actions.left_click()

            # -----------------------------
            # Store latest frame for GUI
            # -----------------------------
            self.latest_frame = annotated

    # -----------------------------
    # Stop Engine Safely
    # -----------------------------
    def stop(self):
        """Stop engine safely and release resources."""
        print("Stopping Gesture Engine...")

        self.running = False

        # Always release drag before exit
        self.actions.stop_drag()

        # Release camera + tracker
        self.camera.release()
        self.tracker.close()

        print("Gesture Engine Stopped.")
