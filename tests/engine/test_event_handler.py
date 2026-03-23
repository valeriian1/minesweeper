import pytest
from unittest.mock import MagicMock, patch
import pygame
from src.engine.event_handler import EventHandler


@pytest.fixture
def mock_game():
    """Фікстура, яка надає мок об'єкт Game."""
    game = MagicMock()
    game.first_click = False
    game.game_over = False
    game.won = False
    game.menu_open = False
    game.best_time = 0
    game.elapsed_time = 0
    return game


@pytest.fixture
def event_handler(mock_game):
    """Фікстура для EventHandler з моком гри."""
    return EventHandler(mock_game)


@pytest.mark.logic
def test_handle_quit_event(event_handler, mock_game):
    """Тест, що pygame.QUIT зупиняє гру."""
    quit_event = MagicMock()
    quit_event.type = pygame.QUIT

    with patch(
        "src.engine.event_handler.pygame.event.get", return_value=[quit_event]
    ):
        event_handler.handle_events()

    assert mock_game.running is False


@pytest.mark.logic
def test_flags_logic_right_click(event_handler, mock_game):
    """Тест встановлення прапорця правим кліком."""
    # Налаштування події
    click_event = MagicMock()
    click_event.type = pygame.MOUSEBUTTONDOWN
    click_event.button = 3  # Правий клік

    # Мок позиції
    pos = (50, 100)
    mock_game.renderer.get_cell_from_pos.return_value = (1, 1)

    # Мокаємо саму клітинку
    mock_cell = MagicMock()
    mock_cell.is_flagged = False
    mock_game.board.grid = {1: {1: mock_cell}}

    with patch(
        "src.engine.event_handler.pygame.mouse.get_pos", return_value=pos
    ), patch(
        "src.engine.event_handler.pygame.event.get", return_value=[click_event]
    ):
        # Виклик обробника подій поля
        event_handler.handle_events()

    # Перевірка виклику toggle_flag
    mock_cell.toggle_flag.assert_called_once()


@pytest.mark.logic
@pytest.mark.parametrize("is_flagged, is_open", [
    (True, False),  # Клітинка з прапорцем
    (False, True),  # Вже відкрита клітинка
])
def test_ignore_clicks_on_flags_or_open(
    event_handler, mock_game, is_flagged, is_open
):
    """Тест ігнорування кліків на відкриті та помічені клітинки."""
    mock_cell = MagicMock()
    mock_cell.is_flagged = is_flagged
    mock_cell.is_open = is_open
    mock_game.board.grid = {0: {0: mock_cell}}

    # Спроба відкрити клітинку
    event_handler._open_cell(0, 0)

    # Перевірка, що генерація та flood_fill не викликалися
    assert not mock_game.board.place_mines.called
    assert not mock_game.board.flood_fill.called


@pytest.mark.logic
def test_recursive_opening_mock_flood_fill(event_handler, mock_game):
    """Тест рекурсивного відкриття порожніх клітинок."""
    mock_cell = MagicMock()
    mock_cell.is_flagged = False
    mock_cell.is_open = False
    mock_cell.is_mine = False
    mock_game.board.grid = {2: {3: mock_cell}}

    event_handler._open_cell(2, 3)

    # Перевірка виклику рекурсивного відкриття
    mock_game.board.flood_fill.assert_called_once_with(2, 3)


@pytest.mark.logic
@pytest.mark.parametrize("state", ["game_over", "won"])
def test_ignore_events_after_game_over(event_handler, mock_game, state):
    """Тест ігнорування кліків після завершення гри."""
    # Встановлюємо стан гри
    if state == "game_over":
        mock_game.game_over = True
    else:
        mock_game.won = True

    # Симулюємо ігнорування кнопки рестарту
    mock_game.renderer.is_restart_clicked.return_value = False

    # Створюємо подію кліку нижче хедера
    pos = (50, 100)
    click_event = MagicMock()
    click_event.type = pygame.MOUSEBUTTONDOWN
    click_event.button = 1

    # Мок взаємодії з полем
    with patch.object(
        event_handler, "_handle_grid_interaction"
    ) as mock_interaction:
        with patch(
            "src.engine.event_handler.pygame.mouse.get_pos", return_value=pos
        ):
            event_handler._handle_mouse_click(click_event)

        mock_interaction.assert_not_called()


@pytest.mark.logic
def test_open_cell_with_mine(event_handler, mock_game):
    """Тест, що відкриття міни змінює стан на game_over."""
    mock_cell = MagicMock()
    mock_cell.is_flagged = False
    mock_cell.is_open = False
    mock_cell.is_mine = True
    mock_game.board.grid = {0: {0: mock_cell}}

    event_handler._open_cell(0, 0)

    assert mock_game.game_over is True
    mock_game.board.reveal_all_mines.assert_called_once()
