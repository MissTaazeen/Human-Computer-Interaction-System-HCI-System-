# src/core/hand_tracker.py

from typing import List, Tuple

import cv2
import mediapipe as mp


class HandTracker:
    """
    HandTracker wraps MediaPipe Hands for the Hand Gesture HCI project.

    Features:
    - Tracks at most ONE hand per frame (max_num_hands=1)
    - Extracts all 21 landmarks
    - Returns landmarks as a list of (id, x, y) in pixel coordinates
    - Draws landmarks and connections on the frame for visualization
    """

    def __init__(
        self,
        max_num_hands: int = 1,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.7,
    ) -> None:
        self._mp_hands = mp.solutions.hands
        self._mp_drawing = mp.solutions.drawing_utils

        # Configure MediaPipe Hands
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def detect(
        self,
        frame_bgr,
        draw: bool = True,
    ) -> Tuple["cv2.Mat", List[Tuple[int, int, int]]]:
        """
        Detect a single hand and extract landmarks.

        Args:
            frame_bgr: Input frame in BGR color space (from OpenCV).
            draw: If True, draw landmarks and connections on the frame.

        Returns:
            output_frame: Frame with landmarks drawn if draw=True, otherwise original frame.
            landmarks: List of (id, x, y) pixel coordinates for 21 landmarks.
                       Returns an empty list if no hand is detected.
        """
        # Convert BGR (OpenCV) → RGB (MediaPipe)
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        # Improve performance: mark image as not writeable during processing
        frame_rgb.flags.writeable = False
        results = self._hands.process(frame_rgb)
        frame_rgb.flags.writeable = True

        output_frame = frame_bgr.copy()
        landmarks: List[Tuple[int, int, int]] = []

        if results.multi_hand_landmarks:
            # For this project phase, use only the first detected hand
            hand_landmarks = results.multi_hand_landmarks[0]

            h, w, _ = output_frame.shape
            for idx, lm in enumerate(hand_landmarks.landmark):
                x_px = int(lm.x * w)
                y_px = int(lm.y * h)
                landmarks.append((idx, x_px, y_px))

            if draw:
                self._mp_drawing.draw_landmarks(
                    image=output_frame,
                    landmark_list=hand_landmarks,
                    connections=self._mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec=self._mp_drawing.DrawingSpec(
                        color=(0, 255, 0),
                        thickness=2,
                        circle_radius=2,
                    ),
                    connection_drawing_spec=self._mp_drawing.DrawingSpec(
                        color=(0, 0, 255),
                        thickness=2,
                    ),
                )

        return output_frame, landmarks

    def close(self) -> None:
        """Release MediaPipe resources."""
        self._hands.close()


def demo() -> None:
    """
    Manual test for the HandTracker class.

    - Opens webcam
    - Detects one hand
    - Draws landmarks
    - Prints number of landmarks
    """
    cap = cv2.VideoCapture(0)
    tracker = HandTracker(max_num_hands=1)

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame, landmarks = tracker.detect(frame, draw=True)

        cv2.putText(
            frame,
            f"Landmarks: {len(landmarks)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("Hand Tracker Demo", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    tracker.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    demo()
