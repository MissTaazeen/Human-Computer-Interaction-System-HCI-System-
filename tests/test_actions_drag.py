from unittest.mock import MagicMock
from core.actions import ActionController


def test_drag_start_calls_mouseDown():
    mock_backend = MagicMock()
    ac = ActionController(backend=mock_backend)

    ac.drag_start()

    mock_backend.mouseDown.assert_called_once_with(button="left")


def test_drag_end_calls_mouseUp():
    mock_backend = MagicMock()
    ac = ActionController(backend=mock_backend)

    ac.drag_end()

    mock_backend.mouseUp.assert_called_once_with(button="left")
