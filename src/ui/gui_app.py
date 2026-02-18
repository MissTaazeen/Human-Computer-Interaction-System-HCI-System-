import sys
import os

# Force Qt to use software rendering (prevents DLL/OpenGL crashes)
os.environ["QT_OPENGL"] = "software"

import mediapipe as mp
print("MediaPipe preloaded successfully")

# Add src/ to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
