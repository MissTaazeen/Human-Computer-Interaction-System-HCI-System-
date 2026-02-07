# src/core/gesture_recognizer.py

"""
GestureRecognizer module for Phase 2 of the Hand Gesture HCI project.

This module provides gesture detection from MediaPipe hand landmarks.
Focus: Pinch gesture detection for click actions with debounce logic.
"""

from typing import List, Tuple, Optional


class GestureRecognizer:
    """
    Recognizes hand gestures from MediaPipe landmarks for gesture-controlled interaction.

    Phase 2 Features:
    - Pinch gesture detection for click actions
    - Debounce logic to detect click events (not continuous pinch state)
    - Configurable threshold for sensitivity tuning
    - Auto-reset on tracking loss (when landmarks disappear)

    Why pinch is ideal for clicking:
    1. Thumb and index are the most precise, dexterous fingers
    2. Distance metric is robust to hand rotation and camera angle
    3. Natural, intuitive interaction (mirrors physical pinching)
    4. Stable and low false-positive rate compared to other gestures
    5. Works across different hand sizes with threshold calibration

    Debounce Logic:
    - Tracks pinch state internally (self.pinch_active)
    - is_pinch() returns raw pinch state (True if thumb and index close)
    - detect_click_event() returns True ONLY on pinch START (transition from False -> True)
    - Auto-resets if hand tracking is lost (empty landmarks)
    - Prevents rapid repeated clicks from continuous pinch holding
    """

    def __init__(self, pinch_threshold: int = 50) -> None:
        """
        Initialize the GestureRecognizer.

        Args:
            pinch_threshold: Maximum pixel distance between thumb tip and index tip
                           for a pinch gesture to be detected.
                           Typical range: 30-80 pixels.
                           Default: 50 pixels (suitable for typical desk setups).
        """
        self._pinch_threshold = pinch_threshold

        # MediaPipe Hands landmark indices for pinch detection
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8

        # Debounce state: tracks whether pinch is currently active
        # Used to detect click events (pinch start) vs continuous pinch state
        self._pinch_active = False

    def _get_point(
        self,
        landmarks: List[Tuple[int, int, int]],
        landmark_id: int,
    ) -> Optional[Tuple[int, int]]:
        """
        Extract a single landmark point from the landmarks list by its ID.

        Args:
            landmarks: List of (id, x, y) tuples from MediaPipe hand detection.
            landmark_id: The landmark ID to search for (0-20 for hands).

        Returns:
            (x, y) pixel coordinates if landmark found, None otherwise.
        """
        for lm_id, x, y in landmarks:
            if lm_id == landmark_id:
                return (x, y)
        return None

    def _euclidean_distance(
        self,
        p1: Tuple[int, int],
        p2: Tuple[int, int],
    ) -> float:
        """
        Compute Euclidean distance between two 2D points.

        Formula: distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)

        Args:
            p1: First point (x1, y1) in pixels.
            p2: Second point (x2, y2) in pixels.

        Returns:
            Distance in pixels as a float.
        """
        x1, y1 = p1
        x2, y2 = p2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def is_pinch(self, landmarks: List[Tuple[int, int, int]]) -> bool:
        """
        Detect if the hand is making a pinch gesture (raw state).

        Pinch Detection Algorithm:
        1. Extract thumb tip landmark (id=4) from the landmarks list
        2. Extract index tip landmark (id=8) from the landmarks list
        3. Compute Euclidean distance between the two points
        4. If distance <= pinch_threshold, return True (pinch detected)
        5. If either landmark is missing or distance > threshold, return False

        Geometry & Stability:
        - Thumb and index naturally converge when pinching
        - Distance metric is independent of hand rotation (only cares about proximity)
        - Works for different hand sizes (calibrate threshold per user if needed)
        - Resistant to lighting changes, hand tilt, and small involuntary movements

        Note: This returns raw pinch state. Use detect_click_event() for debounced clicks.

        Args:
            landmarks: List of (id, x, y) pixel coordinate tuples from hand_tracker.detect()

        Returns:
            True if pinch gesture is detected, False otherwise.
        """
        if not landmarks:
            return False

        # Extract thumb tip and index tip points
        thumb_tip = self._get_point(landmarks, self.THUMB_TIP)
        index_tip = self._get_point(landmarks, self.INDEX_TIP)

        # Both points must be present for pinch detection
        if thumb_tip is None or index_tip is None:
            return False

        # Compute distance and compare against threshold
        distance = self._euclidean_distance(thumb_tip, index_tip)
        return distance <= self._pinch_threshold

    def detect_click_event(self, landmarks: List[Tuple[int, int, int]]) -> bool:
        """
        Detect a click event (pinch START) with debounce logic.

        This method implements state-machine-like behavior:
        - Tracks pinch state in self._pinch_active
        - Returns True ONLY when pinch transitions from False -> True (pinch START)
        - Returns False while pinch is held (continuous state)
        - Returns False when pinch is released
        - Auto-resets if tracking is lost (empty landmarks)

        Debounce Logic:
        Previous state | Current pinch | Return value | Meaning
        ============================================================
        False          | True          | True         | Pinch just started -> CLICK EVENT
        True           | True          | False        | Pinch still held -> no new click
        True           | False         | False        | Pinch just released -> no click
        False          | False         | False        | No pinch -> no click
        (tracking lost)| (any)         | False        | Hand lost -> reset state

        Tracking Loss Handling:
        If landmarks is empty or None, the hand is no longer visible.
        Automatically reset state to prevent false clicks when tracking resumes.

        This prevents rapid repeated clicks from holding pinch continuously.
        Ensures one click per pinch action.

        Args:
            landmarks: List of (id, x, y) pixel coordinate tuples from hand_tracker.detect()

        Returns:
            True if pinch just started (click event detected), False otherwise.
        """
        # Handle tracking loss: if landmarks are empty, reset state
        if not landmarks:
            self.reset_state()
            return False

        # Get current pinch state
        current_pinch = self.is_pinch(landmarks)

        # Detect state transition: False -> True (pinch started)
        click_detected = False
        if current_pinch and not self._pinch_active:
            # Pinch just started
            click_detected = True

        # Update internal state for next frame
        self._pinch_active = current_pinch

        return click_detected

    def reset_state(self) -> None:
        """
        Reset the internal pinch state.

        Use cases:
        - When hand tracking is lost (no landmarks detected)
        - When user switches gestures or modes
        - For debugging or testing

        After reset, the next pinch will be detected as a click event.
        """
        self._pinch_active = False

    def is_pinch_active(self) -> bool:
        """
        Get the current pinch state (debounce state).

        Returns:
            True if pinch is currently active, False otherwise.
        """
        return self._pinch_active

    def set_pinch_threshold(self, threshold: int) -> None:
        """
        Adjust the pinch detection threshold at runtime.

        Use cases:
        - Calibrate to different hand sizes
        - Increase threshold (lower sensitivity) for users with larger hands
        - Decrease threshold (higher sensitivity) for users with smaller hands
        - Fine-tune based on distance from camera

        Args:
            threshold: New pinch threshold in pixels (typically 30-80).
        """
        self._pinch_threshold = threshold

    def get_pinch_threshold(self) -> int:
        """
        Get the current pinch detection threshold.

        Returns:
            Current threshold in pixels.
        """
        return self._pinch_threshold
