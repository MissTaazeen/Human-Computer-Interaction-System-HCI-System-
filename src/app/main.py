import cv2

from core.camera import Camera
from core.hand_tracker import HandTracker
from core.smoothing import Smoother
from core.cursor_mapper import CursorMapper
from core.gesture_recognizer import GestureRecognizer
from core.actions import ActionController
from app import config


def main() -> None:

    camera = Camera(
        device_index=config.CAMERA_INDEX,
        frame_width=config.FRAME_WIDTH,
        frame_height=config.FRAME_HEIGHT,
    )

    hand_tracker = HandTracker(
        max_num_hands=config.MAX_NUM_HANDS,
        detection_confidence=config.DETECTION_CONFIDENCE,
        tracking_confidence=config.TRACKING_CONFIDENCE,
    )

    smoother = Smoother(alpha=config.get_smoothing_alpha())
    cursor_mapper = CursorMapper(smoother=smoother)

    gesture_recognizer = GestureRecognizer(
        pinch_threshold=config.PINCH_THRESHOLD
    )

    action_controller = ActionController()

    drag_active = False

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue

            annotated_frame, landmarks = hand_tracker.detect(frame, draw=True)

            # -----------------------------
            # Cursor Movement
            # -----------------------------
            if landmarks:
                index_points = [
                    lm for lm in landmarks if lm[0] == config.INDEX_FINGER_TIP
                ]

                if index_points:
                    _, x, y = index_points[0]
                    h, w, _ = annotated_frame.shape

                    cursor_mapper.move_cursor(
                        x_frame=x,
                        y_frame=y,
                        frame_width=w,
                        frame_height=h,
                    )

            # -----------------------------
            # Drag Update (EVERY FRAME)
            # -----------------------------
            gesture_recognizer.update_drag_state(landmarks)

            if gesture_recognizer.is_dragging():
                if not drag_active:
                    action_controller.drag_start()
                    drag_active = True
            else:
                if drag_active:
                    action_controller.drag_end()
                    drag_active = False

            # -----------------------------
            # Click Detection (Short Pinch)
            # -----------------------------
            if gesture_recognizer.detect_click_event(landmarks):
                action_controller.left_click()

            # -----------------------------
            # Display ONE Window Only
            # -----------------------------
            cv2.imshow("Hand Gesture HCI", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        if drag_active:
            action_controller.drag_end()

        hand_tracker.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
