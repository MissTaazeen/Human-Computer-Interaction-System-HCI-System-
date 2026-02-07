# src/core/actions.py

"""
ActionController module for Phase 2 of the Hand Gesture HCI project.

This module defines the OS-level action layer.

Phase 2 Scope:
- Only LEFT CLICK action (triggered by pinch gesture)

Design Goals:
- Safe wrapper around PyAutoGUI
- Easy to mock in unit tests
- Minimal responsibilities (gesture logic stays separate)
"""

from __future__ import annotations

from typing import Optional

import pyautogui


class ActionController:
    """
    Executes system-level mouse actions.

    This class is intentionally lightweight:
    - Gesture detection happens elsewhere (GestureRecognizer)
    - This class only performs actions like clicking

    Mock-Friendly Design:
    - PyAutoGUI dependency is injectable for pytest mocking
    """

    def __init__(self, backend: Optional[object] = None) -> None:
        """
        Initialize ActionController.

        Args:
            backend:
                Optional dependency injection for PyAutoGUI.
                In production, defaults to real pyautogui.
                In tests, you can pass a MagicMock.
        """
        self._backend = backend if backend is not None else pyautogui

    def left_click(self) -> None:
        """
        Perform a single left mouse click.

        Triggered only when GestureRecognizer detects a pinch START event.
        """
        self._backend.click(button="left")
