import sys
import threading

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QSlider,
    QCheckBox,
)
from PySide6.QtCore import Qt

from app.main import main
from app.settings_manager import load_settings, save_settings


class GestureApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hand Gesture HCI System")
        self.setFixedSize(500, 400)

        self.settings = load_settings()

        layout = QVBoxLayout()

        # -------------------------------
        # Title
        # -------------------------------
        title = QLabel("Hand Gesture Controlled HCI")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        layout.addWidget(title)

        # -------------------------------
        # Start Button
        # -------------------------------
        self.start_btn = QPushButton("Start Gesture Control")
        self.start_btn.clicked.connect(self.start_engine)
        layout.addWidget(self.start_btn)

        # -------------------------------
        # Pinch Threshold Slider
        # -------------------------------
        self.threshold_label = QLabel(
            f"Pinch Threshold: {self.settings['pinch_threshold']}"
        )
        layout.addWidget(self.threshold_label)

        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(20)
        self.threshold_slider.setMaximum(80)
        self.threshold_slider.setValue(self.settings["pinch_threshold"])
        self.threshold_slider.valueChanged.connect(self.update_threshold)
        layout.addWidget(self.threshold_slider)

        # -------------------------------
        # Enable Click Toggle
        # -------------------------------
        self.click_toggle = QCheckBox("Enable Click Gesture")
        self.click_toggle.setChecked(self.settings["enable_clicks"])
        self.click_toggle.stateChanged.connect(self.update_click_toggle)
        layout.addWidget(self.click_toggle)

        # -------------------------------
        # Save Button
        # -------------------------------
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_all_settings)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    # -------------------------------
    # Run Gesture Engine
    # -------------------------------
    def start_engine(self):
        thread = threading.Thread(target=main)
        thread.daemon = True
        thread.start()

    # -------------------------------
    # Update Threshold Live
    # -------------------------------
    def update_threshold(self, value):
        self.settings["pinch_threshold"] = value
        self.threshold_label.setText(f"Pinch Threshold: {value}")

    def update_click_toggle(self):
        self.settings["enable_clicks"] = self.click_toggle.isChecked()

    def save_all_settings(self):
        save_settings(self.settings)
        self.threshold_label.setText("Settings Saved ✔")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GestureApp()
    window.show()
    sys.exit(app.exec())
