# tests/test_cursor_mapping.py

from unittest.mock import patch, MagicMock

import pytest

from core.cursor_mapper import CursorMapper
from core.smoothing import Smoother


@pytest.fixture
def mock_pyautogui():
    """
    Patch pyautogui.size and pyautogui.moveTo so tests do not
    affect the real mouse cursor.
    """
    with patch("core.cursor_mapper.pyautogui") as mock_pg:
        # Mock screen size to a fixed value for deterministic tests
        mock_pg.size.return_value = (1920, 1080)
        mock_pg.moveTo = MagicMock()
        yield mock_pg


@pytest.fixture
def cursor_mapper(mock_pyautogui):
    """
    CursorMapper instance using a simple Smoother.
    Smoothing is kept but doesn't affect the mapping correctness.
    """
    smoother = Smoother(alpha=1.0)  # alpha=1.0 => no smoothing effect
    return CursorMapper(smoother=smoother)


def test_top_left_maps_near_origin(cursor_mapper, mock_pyautogui):
    """
    Camera coordinates (0, 0) should map close to screen (0, 0).
    """
    frame_width = 640
    frame_height = 480

    # Call move_cursor, which will internally call pyautogui.moveTo
    cursor_mapper.move_cursor(
        x_frame=0,
        y_frame=0,
        frame_width=frame_width,
        frame_height=frame_height,
    )

    # Assert moveTo was called once
    mock_pyautogui.moveTo.assert_called_once()
    x_screen, y_screen = mock_pyautogui.moveTo.call_args[0][:2]

    assert x_screen == pytest.approx(0, abs=1)
    assert y_screen == pytest.approx(0, abs=1)


def test_bottom_right_maps_near_screen_max(cursor_mapper, mock_pyautogui):
    """
    Camera coordinates (frame_width, frame_height) should map close
    to (screen_width, screen_height).
    """
    frame_width = 640
    frame_height = 480
    screen_width, screen_height = mock_pyautogui.size.return_value

    cursor_mapper.move_cursor(
        x_frame=frame_width,
        y_frame=frame_height,
        frame_width=frame_width,
        frame_height=frame_height,
    )

    # Assert moveTo was called again
    assert mock_pyautogui.moveTo.call_count == 2
    x_screen, y_screen = mock_pyautogui.moveTo.call_args[0][:2]

    assert x_screen == pytest.approx(screen_width, abs=1)
    assert y_screen == pytest.approx(screen_height, abs=1)
