# scripts/demo_gesture_manual.py

from core.gesture_recognizer import GestureRecognizer

gr = GestureRecognizer(pinch_threshold=50)

pinch = [(4, 100, 100), (8, 120, 110)]
no_pinch = [(4, 100, 100), (8, 250, 250)]

print("Pinch detected:", gr.is_pinch(pinch))
print("Click event (start):", gr.detect_click_event(pinch))
print("Held pinch (no click):", gr.detect_click_event(pinch))
print("Release:", gr.detect_click_event(no_pinch))
print("Pinch again:", gr.detect_click_event(pinch))
