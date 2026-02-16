import pyautogui


class ActionController:
    """
    Phase 4 Mouse Action Controller

    Supports:
    - Left Click (short pinch)
    - Drag Hold (long pinch hold)

    Uses:
    - mouseDown() for drag start
    - mouseUp() for drag stop
    """

    def __init__(self):
        self.dragging = False

        # Disable PyAutoGUI corner failsafe for stability
        pyautogui.FAILSAFE = False

    # -----------------------------
    # Click
    # -----------------------------
    def left_click(self):
        """Perform a normal left click."""
        pyautogui.click(button="left")

    # -----------------------------
    # Drag Controls
    # -----------------------------
    def start_drag(self):
        """
        Start dragging by holding the left mouse button down.
        Only triggers once.
        """
        if not self.dragging:
            pyautogui.mouseDown(button="left")
            self.dragging = True
            print("Drag Started")

    def stop_drag(self):
        """
        Stop dragging by releasing the left mouse button.
        Only triggers if currently dragging.
        """
        if self.dragging:
            pyautogui.mouseUp(button="left")
            self.dragging = False
            print("Drag Stopped")
