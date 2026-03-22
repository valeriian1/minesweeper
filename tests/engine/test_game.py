import pytest
from unittest.mock import patch
from src.engine.game import Game
from src.utils.constants import DIFFICULTIES
from src.utils.constants import HEADER_HEIGHT


@pytest.fixture
def mock_pygame():
    """Мокаємо залежності Pygame для уникнення вікон під час тестів."""
    with patch("src.engine.game.pygame.init"), \
         patch("src.engine.game.pygame.display.set_mode"), \
         patch("src.engine.game.pygame.display.set_caption"), \
         patch("src.engine.game.GameRenderer"):
        yield


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

    # Перевірка відповідності конфігурації
    config = DIFFICULTIES[difficulty]
    assert game.rows == config["rows"]
    assert game.cols == config["cols"]
    assert game.mines_cnt == config["mines"]


@pytest.mark.game
def test_calculate_window_size(game_instance):
    """Тест розрахунку розміру вікна на основі поля та хедера."""
    width, height = game_instance._calculate_window_size()
    expected_width = game_instance.cols * game_instance.cell_sz
    expected_height = (
        game_instance.rows * game_instance.cell_sz
    ) + HEADER_HEIGHT

    assert width == expected_width
    assert height == expected_height


@pytest.mark.game
def test_reset_game_states(game_instance):
    """Тест скидання станів гри."""
    game_instance.first_click = False
    game_instance.game_over = True
    game_instance.won = True

    game_instance._reset_game_states()

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

    assert game_instance.elapsed_time == 10


@pytest.mark.game
def test_game_update_timer_paused(game_instance):
    """Тест, що таймер не оновлюється після завершення гри."""
    game_instance.first_click = False
    game_instance.start_time = 0
    game_instance.elapsed_time = 5

    game_instance.game_over = True
    game_instance.update()
    assert game_instance.elapsed_time == 5
