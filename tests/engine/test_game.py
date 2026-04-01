import pytest
from unittest.mock import patch
from src.engine.game import Game
from src.utils.constants import DIFFICULTIES


@pytest.fixture
def mock_pygame():
    """Мокаємо залежності Pygame для уникнення вікон під час тестів."""
    with patch("src.engine.game.pygame.init") as mock_i, \
            patch("src.engine.game.pygame.display.set_mode") as mock_sm, \
            patch("src.engine.game.pygame.display.set_caption") as mock_sc, \
            patch("src.engine.game.GameRenderer") as mock_r:
        yield {
            "init": mock_i,
            "set_mode": mock_sm,
            "set_caption": mock_sc,
            "renderer": mock_r
        }


@pytest.fixture
def game_instance(mock_pygame):
    """Фікстура для надання екземпляра Game для тестів."""
    return Game("easy")


@pytest.mark.game
@pytest.mark.parametrize("difficulty", ["easy", "normal", "hard"])
def test_game_init(mock_pygame, difficulty):
    """Тест ініціалізації гри з різними складностями."""
    game = Game(difficulty=difficulty)
    assert game.difficulty == difficulty
    assert game.running is True
    assert game.best_time == 0

    config = DIFFICULTIES[difficulty]
    assert game.rows == config["rows"]
    assert game.cols == config["cols"]
    assert game.mines_cnt == config["mines"]

    mock_pygame["set_mode"].assert_called_once()
    mock_pygame["renderer"].assert_called_once()


@pytest.mark.game
def test_reset_game_states(game_instance):
    """Тест скидання станів гри через публічний метод setup_game."""
    game_instance.first_click = False
    game_instance.game_over = True
    game_instance.won = True
    game_instance.menu_open = True
    game_instance.start_time = 100
    game_instance.elapsed_time = 50

    game_instance.setup_game()

    assert game_instance.first_click is True
    assert game_instance.game_over is False
    assert game_instance.won is False
    assert game_instance.menu_open is False
    assert game_instance.start_time == 0
    assert game_instance.elapsed_time == 0


@pytest.mark.game
@patch("src.engine.game.time.time")
def test_game_update_timer(mock_time, game_instance):
    """Тест оновлення таймера часу під час активної гри."""
    game_instance.first_click = False
    game_instance.game_over = False
    game_instance.won = False

    mock_time.return_value = 100
    game_instance.start_time = 90

    game_instance.update()

    mock_time.assert_called_once()
    assert game_instance.elapsed_time == 10
