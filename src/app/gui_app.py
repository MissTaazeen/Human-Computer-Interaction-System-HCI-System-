import sys
import cv2

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

from core.gesture_engine import GestureEngine


class EngineThread(QThread):
    frame_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.engine = GestureEngine()

    def run(self):
        self.engine.running = True

        while self.engine.running:
            frame = self.engine.camera.get_frame()
            if frame is None:
                continue

            annotated, landmarks = self.engine.tracker.detect(frame, draw=True)

            # Gesture logic
            if landmarks:
                self.engine.recognizer.detect_click_event(landmarks)

            # Emit frame to GUI
            self.frame_signal.emit(annotated)

        self.engine.stop()

    def stop(self):
        self.engine.running = False


class GestureApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hand Gesture Controller - Phase 4")

        self.thread = None

        layout = QVBoxLayout()

        # Camera Display Label
        self.video_label = QLabel("Camera Feed Here")
        layout.addWidget(self.video_label)

        # Buttons
        self.start_btn = QPushButton("Start Controller")
        self.stop_btn = QPushButton("Stop Controller")

        self.start_btn.clicked.connect(self.start_engine)
        self.stop_btn.clicked.connect(self.stop_engine)

        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)

    def start_engine(self):
        if self.thread is None:
            self.thread = EngineThread()
            self.thread.frame_signal.connect(self.update_frame)
            self.thread.start()

    def stop_engine(self):
        if self.thread:
            self.thread.stop()
            self.thread = None

    def update_frame(self, frame):
        """Convert OpenCV frame → Qt image"""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w

        qt_img = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888,
        )

        self.video_label.setPixmap(QPixmap.fromImage(qt_img))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GestureApp()
    window.show()

    sys.exit(app.exec_())
