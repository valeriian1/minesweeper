import pygame
import sys
from src.utils.constants import DIFFICULTIES, HEADER_HEIGHT, BG_COLOR

class Game:
    def __init__(self):
        pygame.init()
        self.difficulty = "easy" 
        self.running = True
        self.setup_game()

    def setup_game(self):
        config = DIFFICULTIES[self.difficulty]
        self.cell_size = config["cell_size"]
        
        width = config["cols"] * self.cell_size
        height = (config["rows"] * self.cell_size) + HEADER_HEIGHT
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Minesweeper - Lab")

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill(BG_COLOR)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        sys.exit()


    