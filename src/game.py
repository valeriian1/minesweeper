import pygame
import sys
import time
from src.core.board import Board
from src.ui.renderer import GameRenderer
from src.utils.constants import DIFFICULTIES, HEADER_HEIGHT, BG_COLOR

class Game:
    def __init__(self):
        pygame.init()
        self.difficulty_names = list(DIFFICULTIES.keys())
        self.current_diff_idx = 0
        self.difficulty = self.difficulty_names[self.current_diff_idx]
        
        self.running = True
        self.first_click = True
        self.game_over = False
        self.won = False
        self.start_time = 0
        self.elapsed_time = 0
        
        self.setup_game()

    def setup_game(self):
        config = DIFFICULTIES[self.difficulty]
        self.rows = config["rows"]
        self.cols = config["cols"]
        self.mines_count = config["mines"]
        self.cell_size = config["cell_size"]
        
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not (self.game_over or self.won):
                pos = pygame.mouse.get_pos()
                
                if pos[1] < HEADER_HEIGHT:
                    if 10 <= pos[0] <= 110: 
                        self.current_diff_idx = (self.current_diff_idx + 1) % len(self.difficulty_names)
                        self.difficulty = self.difficulty_names[self.current_diff_idx]
                        self.setup_game()
                    continue

                grid_pos = self.renderer.get_cell_from_pos(pos)
                if grid_pos:
                    r, c = grid_pos
                    cell = self.board.grid[r][c]
                    
                    if event.button == 1: 
                        if self.first_click:
                            self.board.place_mines(safe_x=c, safe_y=r)
                            self.board.calculate_neighbors()
                            self.first_click = False
                            self.start_time = time.time()
                        
                        if not cell.is_flagged:
                            if cell.is_mine:
                                self.game_over = True
                                self.board.reveal_all_mines()
                            else:
                                self.board.flood_fill(c, r)
                                if self.board.check_win():
                                    self.won = True
                    
                    elif event.button == 3: 
                        cell.toggle_flag()

            elif event.type == pygame.MOUSEBUTTONDOWN and (self.game_over or self.won):
                self.setup_game()

    def update(self):
        if not self.first_click and not self.game_over and not self.won:
            self.elapsed_time = int(time.time() - self.start_time)

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        self.renderer.draw_board(self.board)
        self.renderer.draw_header(
            self.board.get_mines_remaining(), 
            self.elapsed_time, 
            self.difficulty
        )
        
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60) # 60 FPS
        pygame.quit()
        sys.exit()