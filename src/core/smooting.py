from typing import Optional, Tuple


class Smoother:
    """
    Cursor position smoother for gesture-controlled mouse.

    Uses an exponential moving average (EMA)-style update:
        prev + alpha * (target - prev)

    This reduces jitter from noisy hand landmarks while keeping the cursor responsive.
    """

    def __init__(self, alpha: float = 0.2) -> None:
        """
        Args:
            alpha: Smoothing factor in (0, 1].
                   - Smaller alpha  -> more smoothing, more lag.
                   - Larger alpha   -> less smoothing, more responsive.
        """
        if not (0.0 < alpha <= 1.0):
            raise ValueError("alpha must be in the range (0, 1].")

        self._alpha = alpha
        self._prev_x: Optional[float] = None
        self._prev_y: Optional[float] = None

    def reset(self) -> None:
        """Reset internal state (e.g., when tracking is lost)."""
        self._prev_x = None
        self._prev_y = None

    def smooth(self, target_x: float, target_y: float) -> Tuple[float, float]:
        """
        Smooth the incoming cursor target position.

        Args:
            target_x: Raw target x-coordinate (e.g., mapped from hand landmark).
            target_y: Raw target y-coordinate.

        Returns:
            (smooth_x, smooth_y): Smoothed coordinates suitable for cursor movement.
        """
        if self._prev_x is None or self._prev_y is None:
            # First value, no previous state to smooth with.
            self._prev_x = float(target_x)
            self._prev_y = float(target_y)
            return self._prev_x, self._prev_y

        # Exponential moving average update:
        # new = prev + alpha * (target - prev)
        self._prev_x = self._prev_x + self._alpha * (target_x - self._prev_x)
        self._prev_y = self._prev_y + self._alpha * (target_y - self._prev_y)

        return self._prev_x, self._prev_y
