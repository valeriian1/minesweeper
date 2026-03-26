import pygame

from src.ui.assets import AssetManager
from src.utils.constants import (
    DIFFICULTIES,
    CLOSED_CELL_COLOR, CLOSED_CELL_ALPHA,
    OVERLAY_COLOR, OVERLAY_ALPHA,
    ANIM_INTERVAL_HEADER, ANIM_INTERVAL_ENDSCREEN,
    DIGIT_WIDTH,
)


class GameRenderer:
    """
    Відповідає за відображення всіх ігрових елементів:
    поля, хедера, меню складності та екрану кінця гри.
    """

    def __init__(self, screen, cell_size, header_h):
        """
        Ініціалізує рендерер: завантажує ресурси та
        налаштовує параметри відображення.

        Args:
            screen: Поверхня для малювання гри.
            cell_size: Розмір однієї клітинки в пікселях.
            header_h: Висота верхньої панелі.
        """
        self.screen = screen
        self.cell_size = cell_size
        self.header_h = header_h

        # Завантажуємо всі спрайти через AssetManager
        self.assets = AssetManager(cell_size)

        # Напівпрозора маска для закритих клітинок
        self.closed_mask = pygame.Surface((self.cell_size, self.cell_size))
        self.closed_mask.set_alpha(CLOSED_CELL_ALPHA)
        self.closed_mask.fill(CLOSED_CELL_COLOR)

        # Оверлей кінця гри (розмір = розмір вікна)
        sw, sh = screen.get_size()
        self.overlay = pygame.Surface((sw, sh))
        self.overlay.set_alpha(OVERLAY_ALPHA)
        self.overlay.fill(OVERLAY_COLOR)

        # Кнопка рестарту — ініціалізуємо порожнім ректом
        self.btn_rect = pygame.Rect(0, 0, 0, 0)

        # Прямокутники пунктів меню складності
        self.menu_rects: dict[str, pygame.Rect] = {}

    def _get_frame_index(self, interval_ms):
        """Повертає індекс кадру анімації (0 або 1) з заданим інтервалом."""
        return (pygame.time.get_ticks() // interval_ms) % 2

    def get_cell_from_pos(self, pos):
        """
        Перетворює координати кліку миші (x, y) у логічні
          координати сітки (row, col).
        Повертає None, якщо клік був у зоні хедера.

        Args:
            pos: Кортеж (x, y) з координатами кліку миші.
        """
        x, y = pos
        if y < self.header_h:
            return None
        return (y - self.header_h) // self.cell_size, x // self.cell_size

    def draw_board(self, board_obj):
        """
        Відображає ігрове поле на основі стану об'єкта Board.

        Args:
            board_obj: Об'єкт Board з інформацією про клітинки.
        """
        sprites = self.assets.board
        for r in range(board_obj.rows):
            for c in range(board_obj.cols):
                cell = board_obj.grid[r][c]
                x = c * self.cell_size
                y = r * self.cell_size + self.header_h

                base_key = 'tile1' if (r + c) % 2 == 0 else 'tile2'
                self.screen.blit(sprites[base_key], (x, y))

                if cell.is_open:
                    if cell.is_mine:
                        self.screen.blit(sprites['mine'], (x, y))
                    elif cell.adjacent_mines > 0:
                        self.screen.blit(
                            sprites[f'tile{cell.adjacent_mines}a'], (x, y))
                else:
                    self.screen.blit(self.closed_mask, (x, y))
                    if cell.is_flagged:
                        self.screen.blit(sprites['flag'], (x, y))

    def draw_header(self, mines_count, time_seconds, difficulty):
        """
        Відображає верхню панель гри: кнопку вибору складності,
        лічильник мін та таймер.

        Args:
            mines_count: Поточна кількість мін, що залишилися.
            time_seconds: Час, що минув з початку гри, у секундах.
            difficulty: Поточний рівень складності.
        """
        sw = self.screen.get_width()
        center_x = sw // 2
        frame_idx = self._get_frame_index(ANIM_INTERVAL_HEADER)

        # Анімована лінія під хедером
        current_line = self.assets.board_line[frame_idx]
        scaled_line = pygame.transform.scale(current_line, (sw, 20))
        self.screen.blit(scaled_line, (0, self.header_h - 9))

        # Кнопка складності
        self.screen.blit(self.assets.header_frames[frame_idx], (10, 15))
        self.screen.blit(self.assets.diff_labels[difficulty], (10, 15))

        # Лічильник бомб та іконка прапорця
        bomb_x = center_x - 60
        self.screen.blit(self.assets.icon_flag[frame_idx], (bomb_x, 19))
        self._draw_number(mines_count, bomb_x + 35, 20)

        # Таймер
        timer_x = center_x + 50
        self.screen.blit(self.assets.icon_clock[frame_idx], (timer_x, 19))
        self._draw_number(time_seconds, timer_x + 35, 20)

    def _draw_number(self, value, x, y):
        """
        Малює трицифрове число з провідними нулями.

        Args:
            value: Число для відображення (обмежується 0–999).
            x: X-координата початку.
            y: Y-координата початку.
        """
        val = max(0, min(999, value))
        s_value = str(val).zfill(3)
        for i, digit in enumerate(s_value):
            self.screen.blit(self.assets.header_digits[int(
                digit)], (x + i * DIGIT_WIDTH, y))

    def draw_end_screen(self, status, current_time, best_time):
        """
        Відображає вікно кінця гри (перемога або поразка).

        Args:
            status: "win" або "lose" для визначення типу кінцевого екрану.
            current_time: Час, витрачений на поточну гру.
            best_time: Найкращий час сесії.
        """
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Затемнення
        self.screen.blit(self.overlay, (0, 0))

        frame_idx = self._get_frame_index(ANIM_INTERVAL_ENDSCREEN)

        # Базове вікно
        win_img = self.assets.endscreen_frames[frame_idx]
        win_x = (sw - win_img.get_width()) // 2
        win_y = (sh - win_img.get_height()) // 2
        self.screen.blit(win_img, (win_x, win_y))

        # Іконки годинника та трофея
        self.screen.blit(self.assets.trophy_frames[frame_idx], (win_x, win_y))
        self.screen.blit(
            self.assets.icon_clock[frame_idx], (win_x + 40, win_y + 65))

        # В залежності від статусу кінця гри - череп або усміхнене обличчя
        if status == 'lose':
            self.screen.blit(
                self.assets.skull_frames[frame_idx], (win_x, win_y))
        else:
            self.screen.blit(
                self.assets.smiley_frames[frame_idx], (win_x, win_y))

        # Найкращий час та поточний час
        self._draw_number(current_time, win_x + 20, win_y + 110)
        self._draw_number(best_time, win_x + 180, win_y + 110)

        # Кнопка RESTART
        mouse_pos = pygame.mouse.get_pos()
        self.btn_rect = pygame.Rect(win_x + 110, win_y + 110, 75, 50)

        if self.btn_rect.collidepoint(mouse_pos):
            btn_img = self.assets.restart_btn_frames[1]
            draw_x = self.btn_rect.x - 10
        else:
            btn_img = self.assets.restart_btn_frames[0]
            draw_x = self.btn_rect.x - 2

        self.screen.blit(btn_img, (draw_x, self.btn_rect.y))

    def is_restart_clicked(self, pos):
        """
        Перевіряє, чи клік був по кнопці рестарту.

        Args:
            pos: Кортеж (x, y) з координатами кліку миші.

        Returns:
            True, якщо клік був по кнопці рестарту.
        """
        return self.btn_rect.collidepoint(pos)

    def draw_difficulty_menu(self):
        """Відображає випадаюче меню вибору складності."""
        mouse_pos = pygame.mouse.get_pos()
        frame_idx = self._get_frame_index(ANIM_INTERVAL_HEADER)

        menu_x, menu_y = 10, 16
        self.screen.blit(
            self.assets.drop_menu_frames[frame_idx], (menu_x, menu_y))

        options = list(DIFFICULTIES.keys())
        self.menu_rects = {}

        start_y_offset = 31
        line_spacing = 35

        for i, opt in enumerate(options):
            opt_y = menu_y + start_y_offset + (i * line_spacing)

            rect = pygame.Rect(menu_x, opt_y, 120, line_spacing)
            self.menu_rects[opt] = rect

            if rect.collidepoint(mouse_pos):
                self.screen.blit(self.assets.selected_menu,
                                 (rect.x, rect.y - 5))

            self.screen.blit(
                self.assets.diff_labels[opt], (rect.x + 5, rect.y))
