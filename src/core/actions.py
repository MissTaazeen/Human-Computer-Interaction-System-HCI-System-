from __future__ import annotations
from typing import Optional
import pyautogui


class ActionController:
    def __init__(self, backend: Optional[object] = None) -> None:
        self._backend = backend if backend is not None else pyautogui

    def left_click(self) -> None:
        self._backend.click(button="left")

    def drag_start(self) -> None:
        self._backend.mouseDown(button="left")

    def drag_end(self) -> None:
        self._backend.mouseUp(button="left")
