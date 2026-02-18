from typing import Optional

import pyautogui

from core.smoothing import Smoother
from app import config


class CursorMapper:
    """
    Phase 4 Cursor Mapper (Improved)

    Fixes:
    - Cursor too fast → speed scaling added
    - Cursor jump after hand lost → freeze + smooth resume
    """

    def __init__(self, smoother: Optional[Smoother] = None) -> None:
        self._screen_width, self._screen_height = pyautogui.size()
        self._smoother = smoother

        # Freeze control
        self._frozen = False

    # -----------------------------
    # Freeze / Resume
    # -----------------------------
    def freeze(self) -> None:
        """Stop cursor updates when hand is lost."""
        self._frozen = True

    def resume(self) -> None:
        """Resume cursor updates when hand returns."""
        self._frozen = False

    # -----------------------------
    # Mapping
    # -----------------------------
    def _map_to_screen(
        self,
        x_frame: int,
        y_frame: int,
        frame_width: int,
        frame_height: int,
    ) -> tuple[float, float]:

        x_norm = x_frame / float(frame_width)
        y_norm = y_frame / float(frame_height)

        screen_x = x_norm * self._screen_width
        screen_y = y_norm * self._screen_height

        return screen_x, screen_y

    # -----------------------------
    # Cursor Movement (Controlled)
    # -----------------------------
    def move_cursor(
        self,
        x_frame: int,
        y_frame: int,
        frame_width: int,
        frame_height: int,
    ) -> None:

        # If frozen, do nothing
        if self._frozen and config.HAND_LOST_FREEZE:
            return

        # Map → Screen target
        target_x, target_y = self._map_to_screen(
            x_frame, y_frame, frame_width, frame_height
        )

        # Smooth target
        if self._smoother is not None:
            target_x, target_y = self._smoother.smooth(target_x, target_y)

        # Current cursor position
        current_x, current_y = pyautogui.position()

        # Compute movement distance
        dx = target_x - current_x
        dy = target_y - current_y

        distance = (dx**2 + dy**2) ** 0.5

        # -----------------------------
        # DEADZONE FILTER (KEY FIX)
        # -----------------------------
        if distance < config.MOVEMENT_DEADZONE_PX:
            return  # Ignore tiny jitter/noise

        # Speed-controlled movement
        speed = config.CURSOR_SPEED

        new_x = current_x + dx * speed
        new_y = current_y + dy * speed

        pyautogui.moveTo(new_x, new_y)
