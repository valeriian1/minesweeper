import pytest
from unittest.mock import patch, MagicMock
import pygame
from src.ui.renderer import GameRenderer


@pytest.fixture
def mock_asset_manager():
    with patch('src.ui.renderer.AssetManager') as mock_am:
        yield mock_am


@pytest.fixture
def renderer(mock_asset_manager):
    # Мокаємо екран (поверхня pygame)
    screen_mock = MagicMock()
    screen_mock.get_size.return_value = (800, 600)
    screen_mock.get_width.return_value = 800
    screen_mock.get_height.return_value = 600

    # Мокаємо pygame.Surface щоб уникнути помилок в __init__
    with patch('src.ui.renderer.pygame.Surface') as mock_surface:
        surface_instance = MagicMock()
        mock_surface.return_value = surface_instance
        # Створюємо екземпляр рендерера
        r = GameRenderer(screen_mock, cell_size=30, header_h=80)
        yield r, screen_mock, surface_instance, mock_asset_manager


@pytest.mark.ui
@pytest.mark.renderer
@pytest.mark.parametrize("pos, expected", [
    ((150, 50), None),       # Клік в зоні хедера (y < 80)
    ((30, 80), (0, 1)),      # Точно на межі початку дошки (row=0, col=1)
    ((45, 120), (1, 1)),     # Всередині другої клітинки
    ((300, 300), (7, 10)),   # Віддалена клітинка
])
def test_get_cell_from_pos(renderer, pos, expected):
    """Тестує конвертацію екранних координат кліку у
    логічні координати дошки."""
    r, _, _, _ = renderer
    assert r.get_cell_from_pos(pos) == expected


@pytest.mark.ui
@pytest.mark.renderer
@pytest.mark.parametrize("ticks, interval, expected", [
    (100, 400, 0),
    (400, 400, 1),
    (800, 400, 0),
    (999, 500, 1),
])
def test_get_frame_index(renderer, ticks, interval, expected):
    """
    Перевіряє правильність обчислення індексу кадру (0 або 1).
    Мокаємо pygame.time.get_ticks.
    """
    r, _, _, _ = renderer
    with patch('src.ui.renderer.pygame.time.get_ticks', return_value=ticks):
        assert r._get_frame_index(interval) == expected


@pytest.mark.ui
@pytest.mark.renderer
@pytest.mark.parametrize("click_pos, is_colliding", [
    ((125, 125), True),   # Всередині rect
    ((100, 100), True),   # На кутах rect
    ((175, 150), True),
    ((99, 99), False),    # Поза rect
    ((180, 160), False),
])
def test_is_restart_clicked(renderer, click_pos, is_colliding):
    """Тестує спрацьовування кнопки рестарту."""
    r, _, _, _ = renderer
    r.btn_rect = pygame.Rect(100, 100, 76, 51)

    assert r.is_restart_clicked(click_pos) == is_colliding


@pytest.mark.ui
@pytest.mark.renderer
def test_draw_board(renderer):
    """Тестує чи методи малювання викликають правильні
    звернення до екрану об'єкта screen."""
    r, screen_mock, _, mock_am = renderer

    # Мокаємо Board об'єкт
    board_obj_mock = MagicMock()
    board_obj_mock.rows = 2
    board_obj_mock.cols = 2

    # Мок клітинки
    cell_mock_unopened = MagicMock(is_open=False, is_flagged=False)
    cell_mock_opened = MagicMock(is_open=True, is_mine=False, adjacent_mines=0)

    board_obj_mock.grid = [
        [cell_mock_unopened, cell_mock_opened],
        [cell_mock_opened, cell_mock_unopened]
    ]

    # Налаштуємо моки ассетів всередині рендерера
    mock_am_instance = mock_am.return_value
    mock_am_instance.board = {
        'tile1': MagicMock(),
        'tile2': MagicMock(),
    }

    r.draw_board(board_obj_mock)

    # Рендерер повиннен малювати:
    # 4 рази базовий тайл (tile1 або tile2)
    # 2 маски закритої клітинки на unopened
    assert screen_mock.blit.call_count >= 4


@pytest.mark.ui
@pytest.mark.renderer
def test_draw_header(renderer):
    r, screen_mock, _, mock_am = renderer

    mock_am_instance = mock_am.return_value
    mock_am_instance.board_line = [MagicMock(), MagicMock()]
    mock_am_instance.header_frames = [MagicMock(), MagicMock()]
    mock_am_instance.diff_labels = {"easy": MagicMock()}
    mock_am_instance.icon_flag = [MagicMock(), MagicMock()]
    mock_am_instance.icon_clock = [MagicMock(), MagicMock()]
    mock_am_instance.header_digits = [MagicMock() for _ in range(10)]

    with patch('src.ui.renderer.pygame.time.get_ticks', return_value=0), \
            patch('src.ui.renderer.pygame.transform.scale') as _:
        r.draw_header(mines_count=10, time_seconds=45, difficulty="easy")

        # Перевіряємо що відбувається рендеринг елементів хедера на екран
        assert screen_mock.blit.call_count > 0
