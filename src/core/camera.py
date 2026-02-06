# src/core/camera.py

from typing import Optional, Tuple

import cv2


class Camera:
    """
    Wrapper around OpenCV VideoCapture for the Hand Gesture HCI project.

    Features:
    - Initialize webcam capture
    - Provide get_frame() for the latest frame
    - Flip frames horizontally for natural interaction
    - Clean release() method for later phases
    """

    def __init__(
        self,
        device_index: int = 0,
        frame_width: Optional[int] = None,
        frame_height: Optional[int] = None,
    ) -> None:
        """
        Initialize the webcam.

        Args:
            device_index: Index of the camera (0 is default webcam).
            frame_width: Optional desired frame width.
            frame_height: Optional desired frame height.
        """
        self._cap = cv2.VideoCapture(device_index)
        if not self._cap.isOpened():
            raise RuntimeError(f"Could not open camera with index {device_index}")

        # Optionally set desired resolution (if supported by the device)
        if frame_width is not None:
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        if frame_height is not None:
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    def get_frame(self) -> Optional["cv2.Mat"]:
        """
        Read a single frame from the webcam and flip it horizontally.

        Returns:
            frame: BGR image flipped horizontally, or None if capture failed.
        """
        if not self._cap.isOpened():
            return None

        success, frame = self._cap.read()
        if not success or frame is None:
            return None

        # Flip horizontally for mirror-like, natural interaction
        frame_flipped = cv2.flip(frame, 1)  # flipCode=1: horizontal flip[web:36][web:33]

        return frame_flipped

    def release(self) -> None:
        """
        Release the camera resource.
        """
        if self._cap is not None and self._cap.isOpened():
            self._cap.release()  # Properly closes the capturing device[web:37][web:39]


def demo() -> None:
    """
    Simple manual test for the Camera class.
    Opens the webcam, shows flipped frames, and exits on 'q'.
    """
    cam = Camera(device_index=0)

    while True:
        frame = cam.get_frame()
        if frame is None:
            break

        cv2.imshow("Camera Demo (flipped)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    demo()
