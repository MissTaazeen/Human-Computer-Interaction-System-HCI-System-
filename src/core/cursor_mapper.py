from typing import Optional

import pyautogui
from core.smoothing import Smoother 

class CursorMapper:
    """
    Maps hand landmark coordinates (camera frame space) to screen coordinates
    and moves the OS cursor using PyAutoGUI.

    Phase 1:
    - Only cursor movement (no clicking)
    - Designed to be used with the index fingertip landmark
    - Integrates a Smoother instance for stable motion
    """

    def __init__(self, smoother: Optional[Smoother] = None) -> None:
        """
        Args:
            smoother: Optional Smoother instance for cursor stabilization.
                      If None, raw coordinates are used.
        """
        self._screen_width, self._screen_height = pyautogui.size()  # Get primary screen size[web:59][web:60][web:66]
        self._smoother = smoother

    def _map_to_screen(
        self,
        x_frame: int,
        y_frame: int,
        frame_width: int,
        frame_height: int,
    ) -> tuple[float, float]:
        """
        Map camera frame coordinates to screen coordinates.

        Args:
            x_frame: X coordinate in frame pixels.
            y_frame: Y coordinate in frame pixels.
            frame_width: Width of the camera frame in pixels.
            frame_height: Height of the camera frame in pixels.

        Returns:
            (screen_x, screen_y): Coordinates on the primary screen.
        """
        # Normalize to [0, 1]
        x_norm = x_frame / float(frame_width)
        y_norm = y_frame / float(frame_height)

        # Scale to screen size
        screen_x = x_norm * self._screen_width
        screen_y = y_norm * self._screen_height  # Direct mapping; adjust if you use ROI[web:64][web:67]

        return screen_x, screen_y

    def move_cursor(
        self,
        x_frame: int,
        y_frame: int,
        frame_width: int,
        frame_height: int,
    ) -> None:
        """
        Map frame coordinates to screen space, smooth them, and move the cursor.

        Args:
            x_frame: Index fingertip x-coordinate in frame pixels.
            y_frame: Index fingertip y-coordinate in frame pixels.
            frame_width: Width of the current frame.
            frame_height: Height of the current frame.
        """
        # Map camera coordinates → screen coordinates
        screen_x, screen_y = self._map_to_screen(
            x_frame=x_frame,
            y_frame=y_frame,
            frame_width=frame_width,
            frame_height=frame_height,
        )

        # Apply smoothing if provided
        if self._smoother is not None:
            screen_x, screen_y = self._smoother.smooth(screen_x, screen_y)

        # Move the OS cursor (no clicking in Phase 1)
        pyautogui.moveTo(screen_x, screen_y)  # Absolute movement[web:59][web:61][web:68]
