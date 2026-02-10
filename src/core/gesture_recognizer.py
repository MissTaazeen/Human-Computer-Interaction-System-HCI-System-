# src/core/gesture_recognizer.py

"""
GestureRecognizer module (Phase 2)

Features:
- Pinch detection (Thumb + Index)
- Debounced click event (one click per pinch)
- Reset when hand disappears
"""

from typing import List, Tuple, Optional


class GestureRecognizer:
    def __init__(self, pinch_threshold: int = 40) -> None:
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8

        self._pinch_threshold = pinch_threshold
        self._pinch_active = False

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

    def is_pinch(self, landmarks: List[Tuple[int, int, int]]) -> bool:
        if not landmarks:
            return False

        thumb = self._get_point(landmarks, self.THUMB_TIP)
        index = self._get_point(landmarks, self.INDEX_TIP)

        if thumb is None or index is None:
            return False

        return self._distance(thumb, index) <= self._pinch_threshold

    def detect_click_event(self, landmarks: List[Tuple[int, int, int]]) -> bool:
        """
        Returns True only once when pinch starts (False → True transition).
        """

        if not landmarks:
            self.reset_state()
            return False

        current_pinch = self.is_pinch(landmarks)

        click = False
        if current_pinch and not self._pinch_active:
            click = True

        self._pinch_active = current_pinch
        return click

    def reset_state(self) -> None:
        """Reset pinch debounce state."""
        self._pinch_active = False
