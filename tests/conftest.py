import pytest
import pygame
from unittest.mock import MagicMock, patch

from src.engine.game import Game

@pytest.fixture(autouse=True)
def mock_pygame():
    """Mock pygame to run tests in headless mode."""
    with patch("pygame.init") as mock_init, \
         patch("pygame.display.set_mode", return_value=MagicMock()) as mock_set_mode, \
         patch("pygame.display.set_caption") as mock_set_caption, \
         patch("pygame.image.load", return_value=MagicMock()) as mock_load, \
         patch("pygame.font.SysFont", return_value=MagicMock()) as mock_sys_font, \
         patch("pygame.font.Font", return_value=MagicMock()) as mock_font, \
         patch("src.engine.game.GameRenderer") as mock_renderer:
        yield {
            "init": mock_init,
            "set_mode": mock_set_mode,
            "set_caption": mock_set_caption,
            "load": mock_load,
            "sys_font": mock_sys_font,
            "font": mock_font,
            "renderer": mock_renderer
        }

@pytest.fixture
def game_easy():
    """Fixture for an easy difficulty game."""
    return Game(difficulty="easy")

@pytest.fixture
def game_normal():
    """Fixture for a normal difficulty game."""
    return Game(difficulty="normal")

@pytest.fixture
def game_hard():
    """Fixture for a hard difficulty game."""
    return Game(difficulty="hard")
