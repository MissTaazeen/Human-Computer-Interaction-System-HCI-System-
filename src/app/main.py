# src/app/main.py

import cv2

from core.camera import Camera
from core.hand_tracker import HandTracker
from core.smoothing import Smoother
from core.cursor_mapper import CursorMapper
from app import config


def main() -> None:
    # Initialize core components
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

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                break

            # Detect hand and draw landmarks on the frame
            annotated_frame, landmarks = hand_tracker.detect(frame, draw=True)

            # If we have landmarks, use the index fingertip for cursor control
            if landmarks:
                # landmarks is a list of (id, x, y)
                index_points = [lm for lm in landmarks if lm[0] == config.INDEX_FINGER_TIP]

                if index_points:
                    _, x, y = index_points[0]

                    frame_height, frame_width, _ = annotated_frame.shape

                    # Move cursor smoothly using mapped coordinates
                    cursor_mapper.move_cursor(
                        x_frame=x,
                        y_frame=y,
                        frame_width=frame_width,
                        frame_height=frame_height,
                    )

                    # Optional: draw a small circle at the fingertip for clarity
                    cv2.circle(annotated_frame, (x, y), 8, (0, 255, 255), -1)

            # Show the annotated frame
            cv2.imshow("Hand Gesture HCI - Phase 1", annotated_frame)

            # Quit when user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord("q"):  # Common OpenCV pattern[web:76][web:73]
                break
    finally:
        # Clean shutdown
        hand_tracker.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
