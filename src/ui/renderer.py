import pygame
import os

class GameRenderer:
    def __init__(self, screen, cell_size=40, header_h=80):
        self.screen = screen
        self.cell_size = cell_size
        self.header_h = header_h
        
        # Завантажуємо спрайти
        self.sprites = {}
        board_sprite_path = "assets/sprites/board sprites"
        header_sprite_path = "assets/sprites/header sprites"

        self.sprites['tile1'] = pygame.image.load(os.path.join(board_sprite_path, "gridTile1.png"))
        self.sprites['tile2'] = pygame.image.load(os.path.join(board_sprite_path, "gridTile2.png"))
        self.sprites['mine'] = pygame.image.load(os.path.join(board_sprite_path, "TileMine.png"))
        self.sprites['flag'] = pygame.image.load(os.path.join(board_sprite_path, "TileFlagRed.png"))
        self.sprites['tile1a'] = pygame.image.load(os.path.join(board_sprite_path, "Tile1a.png"))
        self.sprites['tile2a'] = pygame.image.load(os.path.join(board_sprite_path, "Tile2a.png"))
        self.sprites['tile3a'] = pygame.image.load(os.path.join(board_sprite_path, "Tile3a.png"))
        self.sprites['tile4a'] = pygame.image.load(os.path.join(board_sprite_path, "Tile4a.png"))
        self.sprites['tile5a'] = pygame.image.load(os.path.join(board_sprite_path, "Tile5a.png"))
        self.sprites['tile6a'] = pygame.image.load(os.path.join(board_sprite_path, "Tile6a.png"))
        self.sprites['tile7a'] = pygame.image.load(os.path.join(board_sprite_path, "Tile7a.png"))
        self.sprites['tile8a'] = pygame.image.load(os.path.join(board_sprite_path, "Tile8a.png"))

        # Анімовані рамки (два кадри)
        self.frame_v1 = pygame.image.load(os.path.join(header_sprite_path, "frame_v1.png"))
        self.frame_v2 = pygame.image.load(os.path.join(header_sprite_path, "frame_v2.png"))
        self.header_frames = [self.frame_v1, self.frame_v2]

        # Іконки (по два кадри)
        self.icon_flag = [pygame.image.load(os.path.join(header_sprite_path, "Flag1.png")),
                          pygame.image.load(os.path.join(header_sprite_path, "Flag2.png"))]
        self.icon_clock = [pygame.image.load(os.path.join(header_sprite_path, "Clock1.png")),
                           pygame.image.load(os.path.join(header_sprite_path, "Clock2.png"))]

        # Цифри для хедера (0-9)
        self.header_digits = [pygame.image.load(os.path.join(header_sprite_path, f"Timer{i}.png")) for i in range(10)]

        # Написи складності
        self.diff_labels = {
            "easy": pygame.image.load(os.path.join(header_sprite_path, "label_easy.png")),
            "medium": pygame.image.load(os.path.join(header_sprite_path, "label_normal.png")),
            "hard": pygame.image.load(os.path.join(header_sprite_path, "label_hard.png"))
        }

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

    def draw_header(self, mines_count, time_seconds, difficulty="easy"):
        # Визначаємо поточний кадр анімації (зміна кожні 400 мс)
        frame_idx = (pygame.time.get_ticks() // 400) % 2
        
        # Малюємо кнопку складності
        self.screen.blit(self.header_frames[frame_idx], (10, 15))
        self.screen.blit(self.diff_labels[difficulty], (10, 15))

        # Малюємо лічильник бомб 
        # Іконка прапорця
        self.screen.blit(self.icon_flag[frame_idx], (110, 19))
        # Малюємо цифри
        self.draw_header_number(mines_count, 140, 20)

        # Малюємо таймер (справа)
        timer_x = self.screen.get_width() - 150 # відступ від правого краю
        self.screen.blit(self.icon_clock[frame_idx], (timer_x + 10, 20))
        self.draw_header_number(time_seconds, timer_x + 50, 20)

    def draw_header_number(self, value, x, y):
        # Перетворюємо число в рядок з провідними нулями до 3 цифр
        s_value = str(value).zfill(3)
        for i, digit in enumerate(s_value):
            digit_idx = int(digit)
            # Малюємо кожну цифру з невеликим відступом одна від одної
            self.screen.blit(self.header_digits[digit_idx], (x + i * 19, y))                
                    