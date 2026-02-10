from typing import List, Tuple, Optional


class GestureRecognizer:
    """
    Phase 3 Gesture Recognizer

    - Short pinch → Click
    - Long pinch hold → Drag
    """

    def __init__(self, pinch_threshold: int = 40) -> None:
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8

        self.PINCH_ON = pinch_threshold
        self.PINCH_OFF = pinch_threshold + 25

        # Frames
        self.CLICK_FRAMES = 6
        self.DRAG_FRAMES = 15

        self._pinch_frames = 0
        self._dragging = False
        self._click_sent = False

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

    def pinch_active(self, landmarks: List[Tuple[int, int, int]]) -> bool:
        if not landmarks:
            return False

        thumb = self._get_point(landmarks, self.THUMB_TIP)
        index = self._get_point(landmarks, self.INDEX_TIP)

        if thumb is None or index is None:
            return False

        return self._distance(thumb, index) <= self.PINCH_ON

    # -----------------------------
    # Click (Short Pinch)
    # -----------------------------
    def detect_click_event(self, landmarks: List[Tuple[int, int, int]]) -> bool:
        if not landmarks:
            self.reset_state()
            return False

        if self.pinch_active(landmarks):

            self._pinch_frames += 1

            if (
                self._pinch_frames == self.CLICK_FRAMES
                and not self._dragging
                and not self._click_sent
            ):
                self._click_sent = True
                return True

        return False

    # -----------------------------
    # Drag (Long Pinch Hold)
    # -----------------------------
    def update_drag_state(self, landmarks: List[Tuple[int, int, int]]) -> None:
        if not landmarks:
            self.reset_state()
            return

        if self.pinch_active(landmarks):

            self._pinch_frames += 1

            if self._pinch_frames >= self.DRAG_FRAMES:
                self._dragging = True

        else:
            self.reset_state()

    def is_dragging(self) -> bool:
        return self._dragging

    # -----------------------------
    # Reset
    # -----------------------------
    def reset_state(self) -> None:
        self._pinch_frames = 0
        self._dragging = False
        self._click_sent = False
