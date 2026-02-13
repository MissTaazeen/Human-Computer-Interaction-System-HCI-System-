from core.camera import Camera
from core.hand_tracker import HandTracker
from core.cursor_mapper import CursorMapper
from core.smoothing import Smoother
from core.gesture_recognizer import GestureRecognizer
from core.actions import ActionController

from app import config


class GestureEngine:
    """
    Runs gesture pipeline without OpenCV display.
    GUI handles visualization.
    """

    def __init__(self):
        self.running = False

        self.camera = Camera()
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

    def start(self):
        """Main loop"""
        self.running = True

        while self.running:
            frame = self.camera.get_frame()
            if frame is None:
                continue

            annotated, landmarks = self.tracker.detect(frame, draw=True)

            # Cursor movement
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

            # Click detection
            if landmarks:
                if self.recognizer.detect_click_event(landmarks):
                    if config.ENABLE_CLICKS:
                        self.actions.left_click()

        self.stop()

    def stop(self):
        self.running = False
        self.camera.release()
        self.tracker.close()
