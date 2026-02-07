#test/test_gesture_recognizer.py

from core.gesture_recognizer import GestureRecognizer


def test_pinch_detected_when_close():
    gr = GestureRecognizer(pinch_threshold=50)
    landmarks = [(4, 100, 100), (8, 120, 110)]
    assert gr.is_pinch(landmarks)


def test_pinch_not_detected_when_far():
    gr = GestureRecognizer(pinch_threshold=50)
    landmarks = [(4, 100, 100), (8, 250, 250)]
    assert not gr.is_pinch(landmarks)


def test_click_event_only_once_per_pinch():
    gr = GestureRecognizer(pinch_threshold=50)

    pinch = [(4, 100, 100), (8, 120, 110)]
    no_pinch = [(4, 100, 100), (8, 250, 250)]

    assert gr.detect_click_event(no_pinch) is False
    assert gr.detect_click_event(pinch) is True
    assert gr.detect_click_event(pinch) is False
    assert gr.detect_click_event(no_pinch) is False
