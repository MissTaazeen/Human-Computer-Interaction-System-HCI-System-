import cv2

from core.camera import Camera
from core.hand_tracker import HandTracker
from core.smoothing import Smoother
from core.cursor_mapper import CursorMapper
from core.gesture_recognizer import GestureRecognizer
from core.actions import ActionController
from app import config


def main() -> None:

    # -----------------------------
    # Initialize Components
    # -----------------------------
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

    # -----------------------------
    # Drag State
    # -----------------------------
    drag_active = False

    try:
        while True:

            # -----------------------------
            # Step 1: Read Frame
            # -----------------------------
            frame = camera.get_frame()
            if frame is None:
                continue

            # -----------------------------
            # Step 2: Detect Hand
            # -----------------------------
            annotated_frame, landmarks = hand_tracker.detect(frame, draw=True)

            # -----------------------------
            # Step 3: Cursor Movement
            # -----------------------------
            if landmarks:
                index_points = [
                    lm for lm in landmarks
                    if lm[0] == config.INDEX_FINGER_TIP
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

                    # Fingertip marker
                    cv2.circle(
                        annotated_frame,
                        (x, y),
                        8,
                        (0, 255, 255),
                        -1,
                    )

            # =====================================================
            # ✅ PHASE 3: DRAG LOGIC (Update FIRST)
            # =====================================================

            gesture_recognizer.update_drag_state(landmarks)

            # -----------------------------
            # Drag Start
            # -----------------------------
            if gesture_recognizer.is_dragging():
                if not drag_active:
                    print("DRAG START")
                    action_controller.drag_start()
                    drag_active = True

            # -----------------------------
            # Drag End
            # -----------------------------
            else:
                if drag_active:
                    print("DRAG END")
                    action_controller.drag_end()
                    drag_active = False

            # =====================================================
            # ✅ PHASE 2: CLICK LOGIC (Only if NOT dragging)
            # =====================================================

            if not drag_active:
                if gesture_recognizer.detect_click_event(landmarks):
                    print("CLICK")
                    action_controller.left_click()

            # -----------------------------
            # Display Window (ONLY ONE)
            # -----------------------------
            cv2.imshow("Hand Gesture HCI - Phase 3", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        # Safety drop
        if drag_active:
            action_controller.drag_end()

        hand_tracker.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
