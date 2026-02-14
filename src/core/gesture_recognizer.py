from typing import List, Tuple, Optional


class GestureRecognizer:
    """
    Phase 4 Gesture Recognizer

    Supports:
    - Click (short pinch)
    - Drag (long pinch hold)
    """

    def __init__(self, pinch_threshold: int = 40) -> None:
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8

        self.PINCH_ON = pinch_threshold
        self.PINCH_OFF = pinch_threshold + 25

        # Timing thresholds
        self.CLICK_HOLD_FRAMES = 3
        self.DRAG_HOLD_FRAMES = 10

        self._pinch_frames = 0
        self._dragging = False
        self._click_sent = False

    # -------------------------------
    # Update Threshold (GUI Slider)
    # -------------------------------
    def update_threshold(self, new_value: int):
        """Update pinch threshold dynamically from GUI"""
        self.PINCH_ON = new_value
        self.PINCH_OFF = new_value + 25

    # -------------------------------
    # Helpers
    # -------------------------------
    def _get_point(
        self,
        landmarks: List[Tuple[int, int, int]],
        landmark_id: int,
    ) -> Optional[Tuple[int, int]]:
        for lm_id, x, y in landmarks:
            if lm_id == landmark_id:
                return (x, y)
        return None

    def _distance(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

    # -------------------------------
    # Pinch Detection
    # -------------------------------
    def pinch_active(self, landmarks) -> bool:
        if not landmarks:
            return False

        thumb = self._get_point(landmarks, self.THUMB_TIP)
        index = self._get_point(landmarks, self.INDEX_TIP)

        if thumb is None or index is None:
            return False

        return self._distance(thumb, index) <= self.PINCH_ON

    # -------------------------------
    # Drag Update
    # -------------------------------
    def update_drag_state(self, landmarks) -> None:
        if not landmarks:
            self.reset_state()
            return

        if self.pinch_active(landmarks):
            self._pinch_frames += 1

            if self._pinch_frames >= self.DRAG_HOLD_FRAMES:
                self._dragging = True
        else:
            self.reset_state()

    def is_dragging(self) -> bool:
        return self._dragging

    # -------------------------------
    # Click Detection
    # -------------------------------
    def detect_click_event(self, landmarks) -> bool:
        """
        Click triggers ONLY if pinch is short
        and drag has NOT started.
        """

        if not landmarks:
            self.reset_state()
            return False

        if self.pinch_active(landmarks):

            self._pinch_frames += 1

            if (
                self._pinch_frames == self.CLICK_HOLD_FRAMES
                and not self._dragging
                and not self._click_sent
            ):
                self._click_sent = True
                return True

        else:
            self.reset_state()

        return False

    # -------------------------------
    # Reset
    # -------------------------------
    def reset_state(self) -> None:
        self._pinch_frames = 0
        self._dragging = False
        self._click_sent = False
