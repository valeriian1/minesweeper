import pytest
from unittest.mock import patch, MagicMock
from src.ui.assets import AssetManager


@pytest.fixture
def mock_pygame():
    with patch('src.ui.assets.pygame') as mock_pg:
        # Створюємо мок-поверхню, яка буде повертатись замість реальних зображень
        mock_surface = MagicMock()
        mock_surface.convert_alpha.return_value = mock_surface

        mock_pg.image.load.return_value = mock_surface
        mock_pg.transform.scale.return_value = mock_surface
        yield mock_pg


@pytest.mark.ui
@pytest.mark.assets
def test_asset_manager_init(mock_pygame):
    """
    Перевіряємо, чи ініціалізується AssetManager,
    чи зберігається розмір клітинки та чи викликається завантаження ресурсів.
    """
    manager = AssetManager(40)
    assert manager.cell_size == 40

    # Перевіряємо, що спрайти дошки завантажились правильно (__init__ викликає _load_board_sprites)
    assert len(manager.board) == 12
    # Перевіряємо завантаження кадрів для хедера та екрана кінця гри
    assert len(manager.header_frames) == 2
    assert len(manager.header_digits) == 10


@pytest.mark.ui
@pytest.mark.assets
@pytest.mark.parametrize("name_prefix, start_idx, count", [
    ("frame_v", 1, 2),
    ("Timer", 0, 10),
    ("Flag", 1, 2),
])
def test_load_frames(mock_pygame, name_prefix, start_idx, count):
    """
    Перевіряємо чи функція _load_frames правильно завантажує очікувану кількість кадрів.
    Використовуємо параметризацію для тестування з різним префіксом і кількістю.
    """
    manager = AssetManager(30)
    # Скидаємо каунтери після __init__
    mock_pygame.image.load.reset_mock()

    frames = manager._load_frames("dummy_path", name_prefix, start_idx, count)

    assert len(frames) == count
    assert mock_pygame.image.load.call_count == count


@pytest.mark.ui
@pytest.mark.assets
def test_load_board_sprites(mock_pygame):
    """
    Перевіряємо чи всі необхідні клітинки ігрового поля завантажились і промасштабувались.
    """
    manager = AssetManager(25)
    mock_pygame.transform.scale.reset_mock()

    board = manager._load_board_sprites()

    # В словнику має бути рівно 12 елементів
    assert len(board) == 12
    # Функція pygame.transform.scale мала бути викликана 12 разів з розміром (25, 25)
    assert mock_pygame.transform.scale.call_count == 12
    for call_args in mock_pygame.transform.scale.call_args_list:
        assert call_args[0][1] == (25, 25)
