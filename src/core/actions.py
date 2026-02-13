# src/core/actions.py

"""
ActionController

Phase 2:
- Left Click

Phase 3:
- Drag Start (mouseDown)
- Drag End (mouseUp)
"""

from __future__ import annotations
from typing import Optional
import pyautogui


class ActionController:
    def __init__(self, backend: Optional[object] = None) -> None:
        self._backend = backend if backend is not None else pyautogui

    def left_click(self) -> None:
        self._backend.click(button="left")

    def drag_start(self) -> None:
        print("DRAG START")
        self._backend.mouseDown(button="left")

    def drag_end(self) -> None:
        print("DRAG END")
        self._backend.mouseUp(button="left")
