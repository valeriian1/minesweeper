import pygame
import time
from src.utils.constants import HEADER_HEIGHT


class EventHandler:
    """
    Обробляє всі вхідні події гри: кліки миші та системні події.
    """

    def __init__(self, game):
        """
        Ініціалізує обробник подій.

        Args:
            game: Посилання на об'єкт Game для зміни ігрового стану.
        """
        self.game = game

    def handle_events(self):
        """
        Обробка подій: вихід з гри та кліки миші.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

    def _handle_mouse_click(self, event):
        """
        Розподіляє кліки між екраном закінчення гри, меню та ігровим полем.
        """
        pos = pygame.mouse.get_pos()

        # Якщо гра закінчена, перевіряємо клік по кнопці рестарту
        if (self.game.game_over or self.game.won) and self.game.renderer.is_restart_clicked(pos):
            self.game.setup_game()
            return

        # Якщо на зоні меню, відкриваємо його відповідно
        if self.game.menu_open:
            if self._handle_menu_interaction(pos):
                return
            self.game.menu_open = False
            return

        if self._is_header_clicked(pos):
            if 10 <= pos[0] <= 110:
                self.game.menu_open = not self.game.menu_open
            return

        # Кліки по ігровому полю
        if pos[1] >= HEADER_HEIGHT:
            self._handle_grid_interaction(event, pos)

    def _is_header_clicked(self, pos):
        """Перевірка кліку в області хедера."""
        return pos[1] < HEADER_HEIGHT

    def _handle_menu_interaction(self, pos):
        """Обробка вибору в меню складності, вибираємо варіант з айтемів класу рендерер."""
        for opt, rect in self.game.renderer.menu_rects.items():
            if rect.collidepoint(pos):
                self.game.difficulty = opt
                self.game.setup_game()
                return True
        return False

    def _handle_grid_interaction(self, event, pos):
        """Кліки по ігровому полю."""
        grid_pos = self.game.renderer.get_cell_from_pos(pos)
        if grid_pos:
            r, c = grid_pos
            if event.button == 1:  # Ліва кнопка миші
                self._open_cell(r, c)
            elif event.button == 3:  # Права кнопка миші
                self.game.board.grid[r][c].toggle_flag()

    def _open_cell(self, row, col):
        """
        Логіка відкриття клітинки з урахуванням першого ходу, 
        наявності або відсутності міни.
        """
        cell = self.game.board.grid[row][col]
        if cell.is_flagged or cell.is_open:
            return

        # Генерація мін після першого кліку
        if self.game.first_click:
            self._generate_board_after_first_click(row, col)

        if cell.is_mine:
            self.game.game_over = True
            self.game.board.reveal_all_mines()
        else:
            self.game.board.flood_fill(row, col)
            self._check_victory_condition()

    def _generate_board_after_first_click(self, row, col):
        """Генерація мін та запуск таймера після початку гри."""
        self.game.board.place_mines(safe_row=row, safe_col=col)
        self.game.board.calculate_neighbors()
        self.game.first_click = False
        self.game.start_time = time.time()

    def _check_victory_condition(self):
        """Перевірка перемоги та оновлення рекорду."""
        if self.game.board.check_win():
            self.game.won = True
            # Оновлюємо рекорд, якщо поточний час кращий за попередній або не дорівнює 0
            if self.game.best_time == 0 or self.game.elapsed_time < self.game.best_time:
                self.game.best_time = self.game.elapsed_time
