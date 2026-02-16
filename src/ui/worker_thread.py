from PyQt5.QtCore import QThread
from core.gesture_engine import GestureEngine


class EngineThread(QThread):
    """
    Runs GestureEngine inside a background thread.
    """

    def __init__(self):
        super().__init__()
        self.engine = GestureEngine()

    def run(self):
        self.engine.start()

    def stop(self):
        self.engine.stop()
