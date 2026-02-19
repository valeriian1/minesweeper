import pygame
import os

from src.utils.constants import DIFFICULTIES, BOARD_SPRITES, HEADER_SPRITES, ENDSCREEN_SPRITES


class AssetManager:
    """
    Завантажує та зберігає всі ігрові спрайти.
    Надає єдину точку доступу до графічних ресурсів.
    """

    def __init__(self, cell_size):
        """
        Завантажує всі ресурси і масштабує їх до потрібного розміру.

        Args:
            cell_size: Розмір клітинки в пікселях (для масштабування тайлів).
        """
        self.cell_size = cell_size

        # Спрайти дошки
        self.board = self._load_board_sprites()

        # Хедер
        self.header_frames = self._load_frames(HEADER_SPRITES, "frame_v", 1, 2)
        self.icon_flag = self._load_frames(HEADER_SPRITES, "Flag", 1, 2)
        self.icon_clock = self._load_frames(HEADER_SPRITES, "Clock", 1, 2)
        self.board_line = self._load_frames(HEADER_SPRITES, "boardLine", 1, 2)
        self.header_digits = self._load_frames(HEADER_SPRITES, "Timer", 0, 10)
        self.drop_menu_frames = self._load_frames(HEADER_SPRITES, "drop_menu", 1, 2)
        self.selected_menu = pygame.image.load(
            os.path.join(HEADER_SPRITES, "selected_menu.png")
        ).convert_alpha()
        self.diff_labels = {
            k: pygame.image.load(
                os.path.join(HEADER_SPRITES, f"label_{k}.png")
            ).convert_alpha()
            for k in DIFFICULTIES.keys()
        }

        # Екран закінчення гри
        self.endscreen_frames = self._load_frames(ENDSCREEN_SPRITES, "window", 1, 2)
        self.trophy_frames = self._load_frames(ENDSCREEN_SPRITES, "trophy", 1, 2)
        self.skull_frames = self._load_frames(ENDSCREEN_SPRITES, "skull", 1, 2)
        self.smiley_frames = self._load_frames(ENDSCREEN_SPRITES, "smileyFace", 1, 2)
        self.restart_btn_frames = self._load_frames(ENDSCREEN_SPRITES, "restart_btn", 1, 2)

    def _load_board_sprites(self):
        """Завантажує та масштабує спрайти ігрового поля."""
        raw_sprites = {
            'tile1': "gridTile1.png", 'tile2': "gridTile2.png",
            'mine': "TileMine.png", 'flag': "TileFlagRed.png",
            'tile1a': "Tile1a.png", 'tile2a': "Tile2a.png",
            'tile3a': "Tile3a.png", 'tile4a': "Tile4a.png",
            'tile5a': "Tile5a.png", 'tile6a': "Tile6a.png",
            'tile7a': "Tile7a.png", 'tile8a': "Tile8a.png",
        }
        return {
            k: pygame.transform.scale(
                pygame.image.load(os.path.join(BOARD_SPRITES, v)).convert_alpha(),
                (self.cell_size, self.cell_size),
            )
            for k, v in raw_sprites.items()
        }

    def _load_frames(self, path, name_prefix, start_index, count):
        """
        Завантажує послідовність кадрів з папки.

        Args:
            path: Шлях до папки з кадрами.
            name_prefix: Префікс назви файлів (без номера та розширення).
            start_index: Початковий номер кадру.
            count: Кількість кадрів для завантаження.

        Returns:
            Список завантажених кадрів як pygame.Surface.
        """
        frames = []
        for i in range(start_index, start_index + count):
            full_path = os.path.join(path, f"{name_prefix}{i}.png")
            img = pygame.image.load(full_path).convert_alpha()
            frames.append(img)
        return frames
