import cv2

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap

from ui.settings_panel import SettingsPanel
from ui.worker_thread import EngineThread


class MainWindow(QWidget):
    """
    Phase 4 Professional Main Window
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hand Gesture Controller - Phase 4")
        self.setGeometry(200, 200, 1000, 600)

        self.thread = None

        # -----------------------------
        # Main Layout
        # -----------------------------
        main_layout = QHBoxLayout()

        # -----------------------------
        # Left Side: Camera Feed
        # -----------------------------
        self.video_label = QLabel("Camera Feed")
        self.video_label.setFixedSize(700, 500)
        self.video_label.setAlignment(Qt.AlignCenter)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.video_label)

        # Status Label
        self.status_label = QLabel("Status: Stopped")
        self.status_label.setStyleSheet("font-size: 14px;")
        left_layout.addWidget(self.status_label)

        # Buttons
        self.start_btn = QPushButton("Start Controller")
        self.stop_btn = QPushButton("Stop Controller")

        self.start_btn.clicked.connect(self.start_engine)
        self.stop_btn.clicked.connect(self.stop_engine)

        left_layout.addWidget(self.start_btn)
        left_layout.addWidget(self.stop_btn)

        # -----------------------------
        # Right Side: Settings Panel
        # -----------------------------
        self.settings_panel = None

        # Add layouts
        main_layout.addLayout(left_layout)

        self.setLayout(main_layout)

        # Timer for webcam updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    # -----------------------------
    # Start Engine
    # -----------------------------
    def start_engine(self):
        if self.thread is None:
            self.thread = EngineThread()
            self.thread.start()

            # Create settings panel now that engine exists
            self.settings_panel = SettingsPanel(self.thread.engine)
            self.layout().addWidget(self.settings_panel)

            self.status_label.setText("Status: Running")
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
        self.status_label.setText("Status: Stopped")

    # -----------------------------
    # Update Frame in QLabel
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
    # Safe Exit
    # -----------------------------
    def closeEvent(self, event):
        self.stop_engine()
        event.accept()
