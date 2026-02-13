from typing import List, Tuple, Optional


class GestureRecognizer:
    """
    Phase 3 Gesture Recognizer

    Supports:
    ✅ Click = quick pinch start (instant)
    ✅ Drag  = pinch held for longer duration
    """

    def __init__(self, pinch_threshold: int = 40) -> None:
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8

        # Pinch thresholds
        self.PINCH_ON = pinch_threshold
        self.PINCH_OFF = pinch_threshold + 25

        # Drag timing
        self.DRAG_HOLD_FRAMES = 8

        # Internal state
        self._pinch_active = False
        self._pinch_frames = 0
        self._dragging = False

    # ------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # Raw Pinch Detection
    # ------------------------------------------------------------
    def is_pinch(self, landmarks: List[Tuple[int, int, int]]) -> bool:
        if not landmarks:
            return False

        thumb = self._get_point(landmarks, self.THUMB_TIP)
        index = self._get_point(landmarks, self.INDEX_TIP)

        if thumb is None or index is None:
            return False

        return self._distance(thumb, index) <= self.PINCH_ON

    # ------------------------------------------------------------
    # CLICK Event (Instant Pinch Start)
    # ------------------------------------------------------------
    def detect_click_event(self, landmarks: List[Tuple[int, int, int]]) -> bool:
        """
        Click happens instantly when pinch starts:
        False → True transition
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

    # ------------------------------------------------------------
    # DRAG State Update (Long Hold)
    # ------------------------------------------------------------
    def update_drag_state(self, landmarks: List[Tuple[int, int, int]]) -> None:
        """
        Drag activates only if pinch is held for DRAG_HOLD_FRAMES.
        """

        if not landmarks:
            self.reset_state()
            return

        if self.is_pinch(landmarks):
            self._pinch_frames += 1

            if self._pinch_frames >= self.DRAG_HOLD_FRAMES:
                self._dragging = True

        else:
            self.reset_state()

    def is_dragging(self) -> bool:
        return self._dragging

    # ------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------
    def reset_state(self) -> None:
        self._pinch_active = False
        self._pinch_frames = 0
        self._dragging = False
