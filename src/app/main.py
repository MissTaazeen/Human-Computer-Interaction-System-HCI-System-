# src/app/main.py

import cv2

from core.camera import Camera
from core.hand_tracker import HandTracker
from core.smoothing import Smoother
from core.cursor_mapper import CursorMapper
from core.gesture_recognizer import GestureRecognizer
from core.actions import ActionController

from app import config


def main() -> None:

    # -------------------------------
    # Initialize Core Components
    # -------------------------------
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

    # -------------------------------
    # Click Feedback + Cooldown
    # -------------------------------
    click_feedback_frames = 0
    click_cooldown = 0

    # -------------------------------
    # Hand Reacquire Delay
    # -------------------------------
    hand_visible = False
    reacquire_frames = 0

    REACQUIRE_DELAY = 6  # wait 6 frames after hand returns

    try:
        while True:

            frame = camera.get_frame()
            if frame is None:
                continue

            annotated_frame, landmarks = hand_tracker.detect(frame, draw=True)

            # -------------------------------
            # HAND LOST → Freeze Cursor
            # -------------------------------
            if not landmarks:
                hand_visible = False
                reacquire_frames = 0
                gesture_recognizer.reset_state()

                cv2.imshow("Hand Gesture HCI - Phase 2", annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

                continue

            # -------------------------------
            # HAND RE-ENTERED → Start Delay
            # -------------------------------
            if not hand_visible:
                hand_visible = True
                reacquire_frames = REACQUIRE_DELAY

            # Reduce delay counter
            if reacquire_frames > 0:
                reacquire_frames -= 1

            # -------------------------------
            # Phase 1: Cursor Movement
            # Only after delay finishes
            # -------------------------------
            if reacquire_frames == 0:

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

                    cv2.circle(
                        annotated_frame,
                        (x, y),
                        8,
                        (0, 255, 255),
                        -1,
                    )

            # -------------------------------
            # Phase 2: Pinch Click Detection
            # -------------------------------
            if click_cooldown > 0:
                click_cooldown -= 1

            if gesture_recognizer.detect_click_event(landmarks):
                if click_cooldown == 0:
                    if config.ENABLE_CLICKS:
                        action_controller.left_click()

                    click_feedback_frames = 10
                    click_cooldown = config.CLICK_COOLDOWN_FRAMES

            # -------------------------------
            # Visual Feedback Overlay
            # -------------------------------
            if click_feedback_frames > 0:
                cv2.putText(
                    annotated_frame,
                    "CLICK",
                    (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 255, 0),
                    4,
                )
                click_feedback_frames -= 1

            # Debug: Reacquire counter
            cv2.putText(
                annotated_frame,
                f"Reacquire: {reacquire_frames}",
                (30, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

            # Show window
            cv2.imshow("Hand Gesture HCI - Phase 2", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        hand_tracker.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
