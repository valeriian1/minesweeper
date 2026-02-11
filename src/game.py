import pygame
import sys
import time
from src.core.board import Board
from src.ui.renderer import GameRenderer
from src.utils.constants import DIFFICULTIES, HEADER_HEIGHT, BG_COLOR

class Game:
    def __init__(self):
        """Ініціалізація основних параметрів та об'єктів гри"""
        pygame.init()
        self.difficulty_names = list(DIFFICULTIES.keys())
        self.current_diff_idx = 0
        self.difficulty = self.difficulty_names[self.current_diff_idx]
        
        self.running = True
        self.setup_game()

    def setup_game(self):
        """Налаштування поля та скидання стану до початкового"""
        config = DIFFICULTIES[self.difficulty]
        self.rows, self.cols = config["rows"], config["cols"]
        self.mines_count, self.cell_size = config["mines"], config["cell_size"]
        
        width = self.cols * self.cell_size
        height = (self.rows * self.cell_size) + HEADER_HEIGHT
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Minesweeper")
        
        self.board = Board(self.rows, self.cols, self.mines_count)
        self.renderer = GameRenderer(self.screen, self.cell_size, HEADER_HEIGHT)
        
        self.first_click = True
        self.game_over = False
        self.won = False
        self.start_time = 0
        self.elapsed_time = 0

    def handle_events(self):
        """Головний диспетчер подій: розділяє технічні події та ігрову логіку."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

    def _handle_mouse_click(self, event):
        """Визначає, куди саме натиснув гравець: у хедер чи на ігрове поле."""
        if self.game_over or self.won:
            self.setup_game() 
            return

        pos = pygame.mouse.get_pos()
        
        if pos[1] < HEADER_HEIGHT:
            self._handle_header_click(pos)
        else:
            self._handle_board_click(pos, event.button)

    def _handle_header_click(self, pos):
        """Логіка натискання на кнопку зміни складності в хедері."""
        if 10 <= pos[0] <= 110: 
            self.current_diff_idx = (self.current_diff_idx + 1) % len(self.difficulty_names)
            self.difficulty = self.difficulty_names[self.current_diff_idx]
            self.setup_game()

    def _handle_board_click(self, pos, mouse_button):
        grid_pos = self.renderer.get_cell_from_pos(pos)
        if not grid_pos:
            return

        r, c = grid_pos
        cell = self.board.grid[r][c]

        if mouse_button == 1: 
            self._open_cell(cell, c, r)  
        elif mouse_button == 3: 
            cell.toggle_flag()

    def _open_cell(self, cell, x, y):  
        if cell.is_flagged:
            return

        if self.first_click:
            self._start_game_logic(x, y) 
        if cell.is_mine:
            self.game_over = True
            self.board.reveal_all_mines()
        else:
            self.board.flood_fill(x, y)
            if self.board.check_win():
                self.won = True

    def _start_game_logic(self, start_x, start_y):
        """Ініціалізація мін та запуск таймера при першому ході."""
        self.board.place_mines(safe_x=start_x, safe_y=start_y)
        self.board.calculate_neighbors()
        self.first_click = False
        self.start_time = time.time()

    def update(self):
        """Оновлення лічильника часу."""
        if not self.first_click and not self.game_over and not self.won:
            self.elapsed_time = int(time.time() - self.start_time)

    def draw(self):
        """Відображення поточного кадру."""
        self.screen.fill(BG_COLOR)
        self.renderer.draw_board(self.board)
        self.renderer.draw_header(self.board.get_mines_remaining(), self.elapsed_time, self.difficulty)
        pygame.display.flip()

    def run(self):
        """Запуск ігрового циклу."""
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        pygame.quit()
        sys.exit()