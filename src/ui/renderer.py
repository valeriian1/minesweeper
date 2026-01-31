import pygame
import os

class GameRenderer:
    def __init__(self, screen, cell_size=40, header_h=120):
        self.screen = screen
        self.cell_size = cell_size
        self.header_h = header_h
        
        # Завантажуємо спрайти
        self.sprites = {}
        sprite_path = "assets/sprites"
        
        self.sprites['tile1'] = pygame.image.load(os.path.join(sprite_path, "gridTile1.png"))
        self.sprites['tile2'] = pygame.image.load(os.path.join(sprite_path, "gridTile2.png"))
        self.sprites['mine'] = pygame.image.load(os.path.join(sprite_path, "TileMine.png"))
        self.sprites['flag'] = pygame.image.load(os.path.join(sprite_path, "TileFlagRed.png"))
        self.sprites['tile1a'] = pygame.image.load(os.path.join(sprite_path, "Tile1a.png"))
        self.sprites['tile2a'] = pygame.image.load(os.path.join(sprite_path, "Tile2a.png"))
        self.sprites['tile3a'] = pygame.image.load(os.path.join(sprite_path, "Tile3a.png"))
        self.sprites['tile4a'] = pygame.image.load(os.path.join(sprite_path, "Tile4a.png"))
        self.sprites['tile5a'] = pygame.image.load(os.path.join(sprite_path, "Tile5a.png"))
        self.sprites['tile6a'] = pygame.image.load(os.path.join(sprite_path, "Tile6a.png"))
        self.sprites['tile7a'] = pygame.image.load(os.path.join(sprite_path, "Tile7a.png"))
        self.sprites['tile8a'] = pygame.image.load(os.path.join(sprite_path, "Tile8a.png"))

    def draw_grid(self, board_data):
        for r, row in enumerate(board_data):
            for c, cell_value in enumerate(row):
                x = c * self.cell_size
                y = r * self.cell_size + self.header_h
                
                base_tile = self.sprites['tile1'] if (r + c) % 2 == 0 else self.sprites['tile2']
                self.screen.blit(base_tile, (x, y))
                
                #тимчасові позначки (змінити при потребі)
                if cell_value == -1: # Міна
                    self.screen.blit(self.sprites['mine'], (x, y))
                elif cell_value == "F": # Прапорець
                    self.screen.blit(self.sprites['flag'], (x, y))
                elif isinstance(cell_value, int) and 1 <= cell_value <= 8:
                    sprite_key = f'tile{cell_value}a'
                    self.screen.blit(self.sprites[sprite_key], (x, y))
                    