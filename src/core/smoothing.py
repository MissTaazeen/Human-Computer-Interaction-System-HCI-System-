from typing import Optional, Tuple


class Smoother:
    """
    Cursor smoothing using Exponential Moving Average (EMA).

    Includes a hard-stop threshold to prevent cursor coasting
    when the hand stops moving.
    """

    def __init__(self, alpha: float = 0.15) -> None:
        if not (0.0 < alpha <= 1.0):
            raise ValueError("alpha must be in range (0, 1].")

        self._alpha = alpha
        self._prev_x: Optional[float] = None
        self._prev_y: Optional[float] = None

    # -----------------------------
    # Helpers
    # -----------------------------
    def has_state(self) -> bool:
        return self._prev_x is not None and self._prev_y is not None

    def reset(self) -> None:
        """Hard reset smoother state."""
        self._prev_x = None
        self._prev_y = None

    # -----------------------------
    # Main Smoothing Function
    # -----------------------------
    def smooth(self, target_x: float, target_y: float) -> Tuple[float, float]:
        """
        Smooth incoming target coordinates.

        Prevents drift/coasting by snapping when movement is tiny.
        """

        # First-time initialization
        if not self.has_state():
            self._prev_x = float(target_x)
            self._prev_y = float(target_y)
            return self._prev_x, self._prev_y

        # Compute distance from current smoothed point to target
        dx = target_x - self._prev_x
        dy = target_y - self._prev_y
        dist = (dx * dx + dy * dy) ** 0.5

        # -----------------------------
        # HARD STOP (Prevents Coasting)
        # -----------------------------
        if dist < 3.0:
            self._prev_x = float(target_x)
            self._prev_y = float(target_y)
            return self._prev_x, self._prev_y

        # Normal EMA update
        self._prev_x = self._prev_x + self._alpha * dx
        self._prev_y = self._prev_y + self._alpha * dy

        return self._prev_x, self._prev_y
