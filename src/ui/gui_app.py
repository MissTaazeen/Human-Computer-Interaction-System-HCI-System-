import sys
import cv2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QCheckBox,
)
from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtGui import QImage, QPixmap

from core.gesture_engine import GestureEngine


# -----------------------------
# Engine Thread
# -----------------------------
class EngineThread(QThread):
    def __init__(self):
        super().__init__()
        self.engine = GestureEngine()

    def run(self):
        self.engine.start()

    def stop(self):
        self.engine.stop()


# -----------------------------
# Main GUI App
# -----------------------------
class GestureApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hand Gesture Controller - Phase 4")
        self.setGeometry(200, 200, 900, 600)

        self.thread = None

        # -----------------------------
        # Layouts
        # -----------------------------
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # -----------------------------
        # Camera Feed Display
        # -----------------------------
        self.video_label = QLabel("Camera Feed")
        self.video_label.setFixedSize(640, 480)

        left_layout.addWidget(self.video_label)

        # -----------------------------
        # Pinch Threshold Slider
        # -----------------------------
        right_layout.addWidget(QLabel("Pinch Sensitivity"))

        self.pinch_slider = QSlider(Qt.Horizontal)
        self.pinch_slider.setMinimum(20)
        self.pinch_slider.setMaximum(80)
        self.pinch_slider.setValue(40)
        self.pinch_slider.valueChanged.connect(self.update_pinch)

        right_layout.addWidget(self.pinch_slider)

        # -----------------------------
        # Click Enable Toggle
        # -----------------------------
        self.click_toggle = QCheckBox("Enable Clicks")
        self.click_toggle.setChecked(True)
        self.click_toggle.stateChanged.connect(self.update_clicks)

        right_layout.addWidget(self.click_toggle)

        # -----------------------------
        # Start/Stop Buttons
        # -----------------------------
        self.start_btn = QPushButton("Start Controller")
        self.stop_btn = QPushButton("Stop Controller")

        self.start_btn.clicked.connect(self.start_engine)
        self.stop_btn.clicked.connect(self.stop_engine)

        right_layout.addWidget(self.start_btn)
        right_layout.addWidget(self.stop_btn)

        # -----------------------------
        # Final Layout Setup
        # -----------------------------
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        # Timer for Frame Updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    # -----------------------------
    # Start Engine
    # -----------------------------
    def start_engine(self):
        if self.thread is None:
            self.thread = EngineThread()
            self.thread.start()

            self.timer.start(30)

    # -----------------------------
    # Stop Engine
    # -----------------------------
    def stop_engine(self):
        if self.thread:
            self.thread.stop()
            self.thread.quit()
            self.thread.wait()
            self.thread = None

        self.timer.stop()
        self.video_label.clear()

    # -----------------------------
    # Update Webcam Feed
    # -----------------------------
    def update_frame(self):
        if self.thread and self.thread.engine.latest_frame is not None:
            frame = self.thread.engine.latest_frame

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            h, w, ch = rgb.shape
            bytes_per_line = ch * w

            qt_image = QImage(
                rgb.data,
                w,
                h,
                bytes_per_line,
                QImage.Format_RGB888,
            )

            pixmap = QPixmap.fromImage(qt_image)

            self.video_label.setPixmap(
                pixmap.scaled(
                    self.video_label.width(),
                    self.video_label.height(),
                    Qt.KeepAspectRatio,
                )
            )

    # -----------------------------
    # Slider Update
    # -----------------------------
    def update_pinch(self):
        if self.thread:
            value = self.pinch_slider.value()
            self.thread.engine.recognizer.update_threshold(value)

    # -----------------------------
    # Click Toggle Update
    # -----------------------------
    def update_clicks(self):
        if self.thread:
            self.thread.engine.enable_clicks = self.click_toggle.isChecked()

    # -----------------------------
    # Close Event Cleanup
    # -----------------------------
    def closeEvent(self, event):
        self.stop_engine()
        event.accept()


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GestureApp()
    window.show()

    sys.exit(app.exec_())
