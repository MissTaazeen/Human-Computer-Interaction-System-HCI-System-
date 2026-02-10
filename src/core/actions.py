# src/core/actions.py

"""
ActionController module (Phase 2)

Only action:
- Left Click
"""

from typing import Optional
import pyautogui


class ActionController:
    def __init__(self, backend: Optional[object] = None) -> None:
        self._backend = backend if backend is not None else pyautogui

    def left_click(self) -> None:
        """Perform a single left mouse click."""
        self._backend.click(button="left")
