# src/core/actions.py

"""
ActionController module for the Hand Gesture HCI project.

Phase 3 Features:
- Left Click
- Drag Start (mouseDown)
- Drag End (mouseUp)

This module is responsible ONLY for OS-level mouse actions.
Gesture recognition remains inside GestureRecognizer.
"""

from __future__ import annotations
from typing import Optional

import pyautogui


class ActionController:
    """
    Executes system-level mouse actions using PyAutoGUI.

    Phase 3 Actions:
    - left_click()
    - drag_start()
    - drag_end()
    """

    def __init__(self, backend: Optional[object] = None) -> None:
        """
        Initialize ActionController.

        Args:
            backend:
                Dependency injection for testing.
                Defaults to real pyautogui in production.
        """
        self._backend = backend if backend is not None else pyautogui

    def left_click(self) -> None:
        """Perform a single left mouse click."""
        self._backend.click(button="left")

    def drag_start(self) -> None:
        """Press and hold the left mouse button (start dragging)."""
        self._backend.mouseDown(button="left")

    def drag_end(self) -> None:
        """Release the left mouse button (drop)."""
        self._backend.mouseUp(button="left")
