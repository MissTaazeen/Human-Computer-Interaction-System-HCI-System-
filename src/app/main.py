# src/app/main.py

"""
Main application runner for the Hand Gesture HCI System.

Phase 2 Features:
- Phase 1: Smooth cursor movement using index fingertip tracking
- Phase 2: Pinch gesture (thumb + index) triggers a LEFT CLICK once per pinch

Modules Used:
- Camera (webcam input)
- HandTracker (MediaPipe landmark detection)
- Smoother (cursor stabilization)
- CursorMapper (frame → screen mapping)
- GestureRecognizer (pinch + debounce click event)
- ActionController (OS-level mouse click)
"""

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

    # Phase 2 components
    gesture_recognizer = GestureRecognizer(
        pinch_threshold=config.PINCH_THRESHOLD
    )
    action_controller = ActionController()

    # Click feedback timer
    click_feedback_frames = 0

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                break

            # Detect hand landmarks
            annotated_frame, landmarks = hand_tracker.detect(frame, draw=True)

            # -------------------------------
            # Phase 1: Cursor Movement
            # -------------------------------
            if landmarks:
                index_points = [
                    lm for lm in landmarks if lm[0] == config.INDEX_FINGER_TIP
                ]

                if index_points:
                    _, x, y = index_points[0]

                    frame_height, frame_width, _ = annotated_frame.shape

                    cursor_mapper.move_cursor(
                        x_frame=x,
                        y_frame=y,
                        frame_width=frame_width,
                        frame_height=frame_height,
                    )

                    # Draw fingertip marker
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
            if landmarks:
                if gesture_recognizer.detect_click_event(landmarks):
                    action_controller.left_click()
                    click_feedback_frames = 10  # show "CLICK" for ~10 frames

            else:
                # Reset pinch state if hand disappears
                gesture_recognizer.reset_state()

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

            # Display window
            cv2.imshow("Hand Gesture HCI - Phase 2 (Pinch Click)", annotated_frame)

            # Quit on 'q'
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        # Clean shutdown
        hand_tracker.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

if gesture_recognizer.detect_click_event(landmarks):
    if config.ENABLE_CLICKS:
        action_controller.left_click()
    click_feedback_frames = 10
