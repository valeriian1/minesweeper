import pygame
import sys
import time
from src.core.board import Board
from src.ui.renderer import GameRenderer
from src.engine.event_handler import EventHandler
from src.utils.constants import DIFFICULTIES, HEADER_HEIGHT, BG_COLOR


class Game:
    def __init__(self, difficulty="easy"):
        """
        Ініціалізація гри: налаштунок параметрів та перший сеанс
        """
        pygame.init()

        # Визначаємо початкову складність
        self.difficulty = difficulty
        self.best_time = 0

        self.running = True
        self.setup_game()

    def setup_game(self):
        """
        Конфігурація ігрового сеансу: створення поля,
        екрану та рендерера.
        Викликається при старті, зміні складності або рестарті
        """
        config = DIFFICULTIES[self.difficulty]
        self.rows, self.cols = config["rows"], config["cols"]
        self.mines_cnt, self.cell_sz = config["mines"], config["cell_size"]

        window_size = self._calculate_window_size()
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Minesweeper")

        # Ініціалізація основних об'єктів
        self.board = Board(self.rows, self.cols, self.mines_cnt)
        self.renderer = GameRenderer(self.screen, self.cell_sz, HEADER_HEIGHT)
        self.event_handler = EventHandler(self)

        # Скидання ігрових станів
        self._reset_game_states()

    def _calculate_window_size(self):
        """Розраховує розмір вікна на основі розміру поля та хедера."""
        width = self.cols * self.cell_sz
        height = (
            self.rows * self.cell_sz) + HEADER_HEIGHT
        return (width, height)

    def _reset_game_states(self):
        """Скидання ігрових станів до початкових значень"""
        self.first_click = True
        self.game_over = False
        self.won = False
        self.menu_open = False
        self.start_time = 0
        self.elapsed_time = 0

    def update(self):
        """
        Оновлення таймера, якщо гра триває
        """
        if not self.first_click and not self.game_over and not self.won:
            self.elapsed_time = int(time.time() - self.start_time)

    def draw(self):
        """
        Відображення всіх елементів гри
        """
        self.screen.fill(BG_COLOR)

        # Малюємо поле та хедер
        self.renderer.draw_board(self.board)
        self.renderer.draw_header(
            self.board.get_mines_remaining(),
            self.elapsed_time,
            self.difficulty)

        # Малюємо екран закінчення, якщо потрібно
        if self.game_over or self.won:
            status = 'lose' if self.game_over else 'win'
            self.renderer.draw_end_screen(
                status, self.elapsed_time, self.best_time)

        # Малюємо меню поверх усього
        if self.menu_open:
            self.renderer.draw_difficulty_menu()

        pygame.display.flip()

    # Визиваємо всі методи тут в головному циклі
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.event_handler.handle_events()
            self.update()
            self.draw()
            clock.tick(60)

        pygame.quit()
        sys.exit()
