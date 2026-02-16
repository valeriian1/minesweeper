import pygame
import sys
import time
from src.core.board import Board
from src.ui.renderer import GameRenderer
from src.utils.constants import DIFFICULTIES, HEADER_HEIGHT, BG_COLOR

class Game:
    def __init__(self):
        """
        Ініціалізація гри: налаштування базових параметрів та запуск першого сеансу
        """
        pygame.init()
        
        # Визначаємо початкову складність
        self.difficulty = "easy"
        self.best_time = 0
        
        self.running = True
        self.setup_game()

    def setup_game(self):
        """
        Конфігурація ігрового сеансу: створення поля, екрану та рендерера
        Викликається при старті, зміні складності або рестарті
        """
        config = DIFFICULTIES[self.difficulty]
        self.rows, self.cols = config["rows"], config["cols"]
        self.mines_cnt, self.cell_sz = config["mines"], config["cell_size"]
        
        # Розрахунок розмірів вікна
        w = self.cols * self.cell_sz
        h = (self.rows * self.cell_sz) + HEADER_HEIGHT
        
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Minesweeper")
        
        # Ініціалізація основних об'єктів
        self.board = Board(self.rows, self.cols, self.mines_cnt)
        self.renderer = GameRenderer(self.screen, self.cell_sz, HEADER_HEIGHT)
        
        # Скидання ігрових станів
        self._reset_game_states()

    def _reset_game_states(self):
        """Скидання ігрових станів до початкових значень"""
        self.first_click = True
        self.game_over = False
        self.won = False
        self.menu_open = False
        self.start_time = 0
        self.elapsed_time = 0

    def handle_events(self):
        """
        Обробка подій: вихід з гри та кліки миші
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

    def _handle_mouse_click(self, event):
        """
        Розподіляє кліки між екраном закінчення гри, меню та ігровим полем
        """
        pos = pygame.mouse.get_pos()

        # Якщо гра закінчена, перевіряємо клік по кнопці рестарту
        if (self.game_over or self.won) and self.renderer.is_restart_clicked(pos):
            self.setup_game()
            return

        # Якщо на зоні меню, відкриваємо його відповідно
        if self.menu_open:
            if self._handle_menu_interaction(pos):
                return
            self.menu_open = False
            return

        if self._is_header_clicked(pos):
            if 10 <= pos[0] <= 110:
                self.menu_open = not self.menu_open
            return
        
        # Кліки по ігровому полю
        if pos[1] >= HEADER_HEIGHT:
            self._handle_grid_interaction(event, pos)

    def _is_header_clicked(self, pos):
        """Перевірка кліку в області хедера"""
        return pos[1] < HEADER_HEIGHT

    def _handle_menu_interaction(self, pos):
        """Обробка вибору в меню складності"""
        for opt, rect in self.renderer.menu_rects.items():
            if rect.collidepoint(pos):
                self.difficulty = opt
                self.setup_game()
                return True
        return False

    def _handle_grid_interaction(self, event, pos):
        """Кліки по ігровому полю"""
        grid_pos = self.renderer.get_cell_from_pos(pos)
        if grid_pos:
            r, c = grid_pos
            if event.button == 1: # Ліва кнопка миші
                self._open_cell(r, c)
            elif event.button == 3: # Права кнопка миші
                self.board.grid[r][c].toggle_flag()

    def _open_cell(self, r, c):
        """
        Логіка відкриття клітинки з урахуванням першого ходу та мін
        """
        cell = self.board.grid[r][c]
        if cell.is_flagged or cell.is_open:
            return

        # Генерація мін після першого кліку
        if self.first_click:
            self._generate_board_after_first_click(r, c)

        if cell.is_mine:
            self.game_over = True
            self.board.reveal_all_mines()
        else:
            self.board.flood_fill(c, r)
            self._check_victory_condition()

    def _generate_board_after_first_click(self, r, c):
        """Генерація мін та запуск таймера"""
        self.board.place_mines(safe_x=c, safe_y=r)
        self.board.calculate_neighbors()
        self.first_click = False
        self.start_time = time.time()

    def _check_victory_condition(self):
        """Перевірка перемоги та оновлення рекорду"""
        if self.board.check_win():
            self.won = True
            # Оновлюємо рекорд, якщо він ще не встановлений або час кращий
            if self.best_time == 0 or self.elapsed_time < self.best_time:
                self.best_time = self.elapsed_time

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
        self.renderer.draw_header(self.board.get_mines_remaining(), self.elapsed_time, self.difficulty)
        
        # Малюємо екран закінчення, якщо потрібно
        if self.game_over or self.won:
            status = 'lose' if self.game_over else 'win'
            self.renderer.draw_end_screen(status, self.elapsed_time, self.best_time)
        
        # Малюємо меню поверх усього
        if self.menu_open:
            self.renderer.draw_difficulty_menu()
            
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()