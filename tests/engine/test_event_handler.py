import pytest
from unittest.mock import create_autospec, patch, MagicMock
import pygame

from src.engine.event_handler import EventHandler
from src.engine.game import Game
from src.core.board import Board
from src.ui.renderer import GameRenderer
from src.core.cell import Cell


@pytest.fixture
def mock_game():
    """
    Фікстура, яка надає безпечний мок
    об'єкт Game зі специфікацією.
    """
    game = create_autospec(Game, instance=True)
    game.first_click = False
    game.game_over = False
    game.won = False
    game.menu_open = False
    game.best_time = 0
    game.elapsed_time = 0

    game.board = create_autospec(Board, instance=True)
    game.renderer = create_autospec(GameRenderer, instance=True)
    return game


@pytest.fixture
def mock_grid(mock_game):
    """Фікстура для створення і встановлення мокованої 2D сітки."""
    grid = [
        [create_autospec(Cell, instance=True) for _ in range(5)]
        for _ in range(5)
    ]
    mock_game.board.grid = grid
    return grid


@pytest.fixture
def event_handler(mock_game):
    """Фікстура для EventHandler з моком гри."""
    return EventHandler(mock_game)


@pytest.mark.logic
def test_handle_quit_event(event_handler, mock_game):
    """Тест, що pygame.QUIT зупиняє гру."""
    quit_event = MagicMock()
    quit_event.type = pygame.QUIT

    patch_path = "src.engine.event_handler.pygame.event.get"
    with patch(patch_path, return_value=[quit_event]):
        event_handler.handle_events()

    assert mock_game.running is False


@pytest.mark.logic
def test_flags_logic_right_click(event_handler, mock_game, mock_grid):
    """
    Тест встановлення прапорця правим кліком
    через публічний інтерфейс.
    """
    click_event = MagicMock()
    click_event.type = pygame.MOUSEBUTTONDOWN
    click_event.button = 3

    pos = (50, 100)
    mock_game.renderer.get_cell_from_pos.return_value = (1, 1)

    mock_cell = mock_grid[1][1]
    mock_cell.is_flagged = False

    patch_pos = "src.engine.event_handler.pygame.mouse.get_pos"
    patch_event = "src.engine.event_handler.pygame.event.get"

    with patch(patch_pos, return_value=pos), \
            patch(patch_event, return_value=[click_event]):
        event_handler.handle_events()

    mock_cell.toggle_flag.assert_called_once()


@pytest.mark.logic
@pytest.mark.parametrize("is_flagged, is_open", [
    (True, False),
    (False, True),
])
def test_ignore_clicks_on_flags_or_open(
    event_handler, mock_game, mock_grid, is_flagged, is_open
):
    """
    Тест ігнорування кліків лівою кнопкою на відкриті
    та помічені клітинки через handle_events.
    """
    click_event = MagicMock()
    click_event.type = pygame.MOUSEBUTTONDOWN
    click_event.button = 1

    pos = (50, 100)
    mock_game.renderer.get_cell_from_pos.return_value = (0, 0)

    mock_cell = mock_grid[0][0]
    mock_cell.is_flagged = is_flagged
    mock_cell.is_open = is_open

    patch_pos = "src.engine.event_handler.pygame.mouse.get_pos"
    patch_event = "src.engine.event_handler.pygame.event.get"

    with patch(patch_pos, return_value=pos), \
            patch(patch_event, return_value=[click_event]):
        event_handler.handle_events()

    mock_game.board.place_mines.assert_not_called()
    mock_game.board.flood_fill.assert_not_called()


@pytest.mark.logic
@pytest.mark.parametrize("state", ["game_over", "won"])
def test_ignore_events_after_game_over(event_handler, mock_game, state):
    """Тест ігнорування кліків по полю після завершення гри."""
    if state == "game_over":
        mock_game.game_over = True
    else:
        mock_game.won = True

    mock_game.renderer.is_restart_clicked.return_value = False

    click_event = MagicMock()
    click_event.type = pygame.MOUSEBUTTONDOWN
    click_event.button = 1
    pos = (50, 100)

    patch_pos = "src.engine.event_handler.pygame.mouse.get_pos"
    patch_event = "src.engine.event_handler.pygame.event.get"
    mock_interaction = "_handle_grid_interaction"

    with patch.object(event_handler, mock_interaction) as mi, \
            patch(patch_pos, return_value=pos), \
            patch(patch_event, return_value=[click_event]):
        event_handler.handle_events()

    mi.assert_not_called()


@pytest.mark.logic
def test_open_cell_with_mine(event_handler, mock_game, mock_grid):
    """Тест, що клік по міні повністю зупиняє гру та показує міни."""
    click_event = MagicMock()
    click_event.type = pygame.MOUSEBUTTONDOWN
    click_event.button = 1

    pos = (50, 100)
    mock_game.renderer.get_cell_from_pos.return_value = (0, 0)

    mock_cell = mock_grid[0][0]
    mock_cell.is_flagged = False
    mock_cell.is_open = False
    mock_cell.is_mine = True

    patch_pos = "src.engine.event_handler.pygame.mouse.get_pos"
    patch_event = "src.engine.event_handler.pygame.event.get"

    with patch(patch_pos, return_value=pos), \
            patch(patch_event, return_value=[click_event]):
        event_handler.handle_events()

    assert mock_game.game_over is True
    mock_game.board.reveal_all_mines.assert_called_once()


@pytest.mark.logic
@patch("src.engine.event_handler.time.time")
def test_first_click_logic(mock_time, event_handler, mock_game, mock_grid):
    """
    Тест логіки першого кліку: розміщення мін,
    підрахунок сусідів, старт таймера.
    """
    mock_time.return_value = 1234.5
    mock_game.first_click = True

    click_event = MagicMock()
    click_event.type = pygame.MOUSEBUTTONDOWN
    click_event.button = 1

    pos = (50, 100)
    mock_game.renderer.get_cell_from_pos.return_value = (2, 2)

    mock_cell = mock_grid[2][2]
    mock_cell.is_flagged = False
    mock_cell.is_open = False
    mock_cell.is_mine = False

    patch_pos = "src.engine.event_handler.pygame.mouse.get_pos"
    patch_event = "src.engine.event_handler.pygame.event.get"

    with patch(patch_pos, return_value=pos), \
            patch(patch_event, return_value=[click_event]):
        event_handler.handle_events()

    mock_game.board.place_mines.assert_called_once_with(
        safe_row=2, safe_col=2
    )
    mock_game.board.calculate_neighbors.assert_called_once()
    assert mock_game.first_click is False
    assert mock_game.start_time == 1234.5
    mock_game.board.flood_fill.assert_called_once_with(2, 2)
