from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSlider,
    QCheckBox,
)
from PyQt5.QtCore import Qt

from app import config


class SettingsPanel(QWidget):
    """
    Phase 4 Settings Panel

    Controls:
    - Pinch Sensitivity Threshold
    - Cursor Speed Adjustment
    - Enable/Disable Clicks
    - Enable/Disable Drag
    """

    def __init__(self, engine):
        super().__init__()

        self.engine = engine

        layout = QVBoxLayout()

        # -----------------------------
        # Pinch Sensitivity Slider
        # -----------------------------
        layout.addWidget(QLabel("Pinch Sensitivity Threshold"))

        self.pinch_slider = QSlider(Qt.Horizontal)
        self.pinch_slider.setMinimum(20)
        self.pinch_slider.setMaximum(80)
        self.pinch_slider.setValue(config.PINCH_THRESHOLD)

        self.pinch_slider.valueChanged.connect(self.update_pinch)

        layout.addWidget(self.pinch_slider)

        # -----------------------------
        # Cursor Speed Slider
        # -----------------------------
        layout.addWidget(QLabel("Cursor Speed"))

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(10)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(int(config.CURSOR_SPEED * 100))

        self.speed_slider.valueChanged.connect(self.update_speed)

        layout.addWidget(self.speed_slider)

        # -----------------------------
        # Click Enable Toggle
        # -----------------------------
        self.click_toggle = QCheckBox("Enable Clicks")
        self.click_toggle.setChecked(config.ENABLE_CLICKS)

        self.click_toggle.stateChanged.connect(self.update_clicks)

        layout.addWidget(self.click_toggle)

        # -----------------------------
        # Drag Enable Toggle
        # -----------------------------
        self.drag_toggle = QCheckBox("Enable Drag")
        self.drag_toggle.setChecked(True)

        self.drag_toggle.stateChanged.connect(self.update_drag)

        layout.addWidget(self.drag_toggle)

        layout.addStretch()
        self.setLayout(layout)

    # -----------------------------
    # Update Pinch Threshold
    # -----------------------------
    def update_pinch(self):
        value = self.pinch_slider.value()
        self.engine.recognizer.update_threshold(value)

    # -----------------------------
    # Update Cursor Speed
    # -----------------------------
    def update_speed(self):
        value = self.speed_slider.value()
        config.CURSOR_SPEED = value / 100.0
        print("Cursor Speed Updated:", config.CURSOR_SPEED)

    # -----------------------------
    # Update Click Toggle
    # -----------------------------
    def update_clicks(self):
        self.engine.enable_clicks = self.click_toggle.isChecked()
        print("Clicks Enabled:", self.engine.enable_clicks)

    # -----------------------------
    # Update Drag Toggle
    # -----------------------------
    def update_drag(self):
        self.engine.enable_drag = self.drag_toggle.isChecked()
        print("Drag Enabled:", self.engine.enable_drag)
