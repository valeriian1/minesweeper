import pygame
import os

class GameRenderer:
    def __init__(self, screen, cell_size, header_h):
        """
        Ініціалізує рендерер: завантажує ресурси та налаштовує параметри відображення.
        """
        self.screen = screen
        self.cell_size = cell_size
        self.header_h = header_h

        # Створюємо напівпрозору маску для відкритих клітинок
        self.open_mask = pygame.Surface((self.cell_size, self.cell_size))
        self.open_mask.set_alpha(80)
        self.open_mask.fill((0, 0, 50))

        # Завантажуємо спрайти
        board_sprite_path = "assets/sprites/board sprites"
        header_sprite_path = "assets/sprites/header sprites"

        raw_sprites = {
            'tile1': "gridTile1.png", 'tile2': "gridTile2.png",
            'mine': "TileMine.png", 'flag': "TileFlagRed.png",
            'tile1a': "Tile1a.png", 'tile2a': "Tile2a.png",
            'tile3a': "Tile3a.png", 'tile4a': "Tile4a.png",
            'tile5a': "Tile5a.png", 'tile6a': "Tile6a.png",
            'tile7a': "Tile7a.png", 'tile8a': "Tile8a.png"
        }
        
        self.sprites = {}
        for key, filename in raw_sprites.items():
            img = pygame.image.load(os.path.join(board_sprite_path, filename)).convert_alpha()
            # Масштабуємо спрайти до розміру клітинки
            self.sprites[key] = pygame.transform.scale(img, (self.cell_size, self.cell_size))

        # Хедерні спрайти
        self.header_frames = [
            pygame.image.load(os.path.join(header_sprite_path, "frame_v1.png")).convert_alpha(),
            pygame.image.load(os.path.join(header_sprite_path, "frame_v2.png")).convert_alpha()
        ]
        
        self.icon_flag = [
            pygame.image.load(os.path.join(header_sprite_path, "Flag1.png")).convert_alpha(),
            pygame.image.load(os.path.join(header_sprite_path, "Flag2.png")).convert_alpha()
        ]
        
        self.icon_clock = [
            pygame.image.load(os.path.join(header_sprite_path, "Clock1.png")).convert_alpha(),
            pygame.image.load(os.path.join(header_sprite_path, "Clock2.png")).convert_alpha()
        ]

        self.header_digits = [
            pygame.image.load(os.path.join(header_sprite_path, f"Timer{i}.png")).convert_alpha() 
            for i in range(10)
        ]

        self.diff_labels = {
            k: pygame.image.load(os.path.join(header_sprite_path, f"label_{v}.png")).convert_alpha()
            for k, v in [("easy", "easy"), ("normal", "normal"), ("hard", "hard")]
        }

        self.board_line = [
            pygame.image.load(os.path.join(header_sprite_path, "boardLine1.png")).convert_alpha(),
            pygame.image.load(os.path.join(header_sprite_path, "boardLine2.png")).convert_alpha()
        ]

    def get_cell_from_pos(self, pos):
        """
        Перетворює координати кліку миші (x, y) у логічні координати сітки (row, col).
        Повертає None, якщо клік був у зоні хедера.
        """
        x, y = pos
        if y < self.header_h: return None
        return (y - self.header_h) // self.cell_size, x // self.cell_size

    # Малюємо ігрове поле
    def draw_board(self, board_obj):
        for r in range(board_obj.rows):
            for c in range(board_obj.cols):
                cell = board_obj.grid[r][c] # беремо об'єкт клітинки
                x = c * self.cell_size
                y = r * self.cell_size + self.header_h
                
                base_key = 'tile1' if (r + c) % 2 == 0 else 'tile2'
                self.screen.blit(self.sprites[base_key], (x, y))
                
                # Якщо клітинка відкрита
                if cell.is_open:
                    self.screen.blit(self.open_mask, (x, y))
                    
                    if cell.is_mine:
                        self.screen.blit(self.sprites['mine'], (x, y))
                    elif cell.adjacent_mines > 0:
                        self.screen.blit(self.sprites[f'tile{cell.adjacent_mines}a'], (x, y))
                
                # Якщо стоїть прапорець
                elif cell.is_flagged:
                    self.screen.blit(self.sprites['flag'], (x, y))
    
    def draw_header(self, mines_count, time_seconds, difficulty):
        """
        Відображає верхню панель гри: кнопку вибору складності, 
        лічильник мін та таймер.
        """
        sw = self.screen.get_width()
        center_x = sw // 2
        # Визначаємо поточний кадр анімації (зміна кожні 400 мс)
        frame_idx = (pygame.time.get_ticks() // 400) % 2
        
        # Малюємо анімовану лінію під хедером
        current_line = self.board_line[frame_idx]
        scaled_line = pygame.transform.scale(current_line, (sw, 20))
        self.screen.blit(scaled_line, (0, self.header_h - 9))

        # Малюємо кнопку складності
        self.screen.blit(self.header_frames[frame_idx], (10, 15))
        self.screen.blit(self.diff_labels[difficulty], (10, 15))

        # Малюємо лічильник бомб 
        # Іконка прапорця
        bomb_x = center_x - 60
        self.screen.blit(self.icon_flag[frame_idx], (bomb_x, 19))
        self.draw_header_number(mines_count, bomb_x + 35, 20)

        # Малюємо таймер
        timer_x = center_x + 50
        self.screen.blit(self.icon_clock[frame_idx], (timer_x, 19))
        self.draw_header_number(time_seconds, timer_x + 35, 20)

    def draw_header_number(self, value, x, y):
        """
        Малює числа у хедері
        """
        val = max(0, min(999, value)) # Обмежуємо від 0 до 999
        # Перетворюємо число в рядок з провідними нулями до 3 цифр
        s_value = str(val).zfill(3)
        for i, digit in enumerate(s_value):
            self.screen.blit(self.header_digits[int(digit)], (x + i * 19, y))