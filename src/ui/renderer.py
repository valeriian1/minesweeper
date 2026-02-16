import pygame
import os

from src.utils.constants import DIFFICULTIES

class GameRenderer:

    def load_frames(self, path, name_prefix, count):
        """
        Завантажує n кадрів з папки за шаблоном назви
        
        Args:
            path (str): Шлях до папки з кадрами.
            name_prefix (str): Загальна частина назви файлів кадрів (без номера та розширення).
            count (int): Кількість кадрів для завантаження.
        Returns:
            list: Список завантажених кадрів у вигляді pygame.Surface.
        """
        frames = []
        for i in range(1, count + 1):
            full_path = os.path.join(path, f"{name_prefix}{i}.png")
            img = pygame.image.load(full_path).convert_alpha()
            frames.append(img)
        return frames
        

    def __init__(self, screen, cell_size, header_h):
        """
        Ініціалізує рендерер: завантажує ресурси та налаштовує параметри відображення

        Args:
            screen (pygame.Surface): Поверхня для малювання гри.
            cell_size (int): Розмір однієї клітинки в пікселях.
            header_h (int): Висота верхньої панелі.
        """
        self.screen = screen
        self.cell_size = cell_size
        self.header_h = header_h

        # Створюємо напівпрозору маску для закритих клітинок
        self.closed_mask = pygame.Surface((self.cell_size, self.cell_size))
        self.closed_mask.set_alpha(120)
        self.closed_mask.fill((0, 0, 120))

        # Створюємо напівпрозору чорну оверлей поверх всього екрану (для віконця кінець гри)
        self.overlay = pygame.Surface((1000, 1000))
        self.overlay.set_alpha(180)
        self.overlay.fill((0, 0, 0))

        # Завантажуємо спрайти
        board_sprite_path = "assets/sprites/board sprites"
        header_sprite_path = "assets/sprites/header sprites"
        endscreen_sprite_path = "assets/sprites/endscreen sprites"

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
        self.header_frames = self.load_frames(header_sprite_path, "frame_v", 2)
        
        self.icon_flag = self.load_frames(header_sprite_path, "Flag", 2)
        
        self.icon_clock = self.load_frames(header_sprite_path, "Clock", 2)

        self.header_digits = [
            pygame.image.load(os.path.join(header_sprite_path, f"Timer{i}.png")).convert_alpha() 
            for i in range(10)
        ]

        self.diff_labels = {
            k: pygame.image.load(os.path.join(header_sprite_path, f"label_{v}.png")).convert_alpha()
            for k, v in [("easy", "easy"), ("normal", "normal"), ("hard", "hard")]
        }

        self.board_line = self.load_frames(header_sprite_path, "boardLine", 2)

        self.drop_menu_frames = self.load_frames(header_sprite_path, "drop_menu", 2)

        self.selected_menu = pygame.image.load(os.path.join(header_sprite_path, "selected_menu.png")).convert_alpha()

        self.endscreen_frames = self.load_frames(endscreen_sprite_path, "window", 2)

        self.trophy_frames = self.load_frames(endscreen_sprite_path, "trophy", 2)
        
        self.skull_frames = self.load_frames(endscreen_sprite_path, "skull", 2)

        self.smiley_frames = self.load_frames(endscreen_sprite_path, "smileyFace", 2)

        self.restart_btn_frames = self.load_frames(endscreen_sprite_path, "restart_btn", 2)

    def get_cell_from_pos(self, pos):
        """
        Перетворює координати кліку миші (x, y) у логічні координати сітки (row, col).
        Повертає None, якщо клік був у зоні хедера.

        Args:
            pos (tuple): Кортеж (x, y) з координатами кліку миші.
        """
        x, y = pos
        if y < self.header_h: 
            return None
        return (y - self.header_h) // self.cell_size, x // self.cell_size

    def draw_board(self, board_obj):
        """ 
        Відображає ігрове поле на основі стану об'єкта Board. 
        Args:
            board_obj (Board): Об'єкт, що містить інформацію про клітинки
        """
        for r in range(board_obj.rows):
            for c in range(board_obj.cols):
                cell = board_obj.grid[r][c] # беремо об'єкт клітинки
                x = c * self.cell_size
                y = r * self.cell_size + self.header_h
                
                base_key = 'tile1' if (r + c) % 2 == 0 else 'tile2'
                self.screen.blit(self.sprites[base_key], (x, y))
                
                # Якщо клітинка відкрита
                if cell.is_open:
                    if cell.is_mine:
                        self.screen.blit(self.sprites['mine'], (x, y))
                    elif cell.adjacent_mines > 0:
                        self.screen.blit(self.sprites[f'tile{cell.adjacent_mines}a'], (x, y))
                
                # Якщо клітинка закрита
                else:
                    self.screen.blit(self.closed_mask, (x, y))
                    # Якщо стоїть прапорець
                    if cell.is_flagged:
                        self.screen.blit(self.sprites['flag'], (x, y))
    
    def draw_header(self, mines_count, time_seconds, difficulty):
        """
        Відображає верхню панель гри: кнопку вибору складності, 
        лічильник мін та таймер.

        Args:
            mines_count (int): Поточна кількість мін, що залишилися.
            time_seconds (int): Час, що минув з початку гри, у секундах.
            difficulty (str): Поточний рівень складності.
        """
        sw = self.screen.get_width()
        center_x = sw // 2
        # Визначаємо поточний кадр анімації (зміна кожні 400 мс)
        frame_idx = (pygame.time.get_ticks() // 400) % 2
        
        # Анімована лінія під хедером
        current_line = self.board_line[frame_idx]
        scaled_line = pygame.transform.scale(current_line, (sw, 20))
        self.screen.blit(scaled_line, (0, self.header_h - 9))

        # Кнопка складності
        self.screen.blit(self.header_frames[frame_idx], (10, 15))
        self.screen.blit(self.diff_labels[difficulty], (10, 15))

        # Лічильник бомб та іконка прапорця
        bomb_x = center_x - 60
        self.screen.blit(self.icon_flag[frame_idx], (bomb_x, 19))
        self.draw_header_number(mines_count, bomb_x + 35, 20)

        # Таймер
        timer_x = center_x + 50
        self.screen.blit(self.icon_clock[frame_idx], (timer_x, 19))
        self.draw_header_number(time_seconds, timer_x + 35, 20)

    def draw_header_number(self, value, x, y):
        """
        Малює числа у хедері

        Args:
            value (int): Число для відображення (кількість мін або часу)
            x (int): X-координата початку відображення числа
            y (int): Y-координата початку відображення числа
        """
        val = max(0, min(999, value)) # Обмежуємо від 0 до 999
        # Перетворюємо число в рядок з провідними нулями до 3 цифр
        s_value = str(val).zfill(3)
        for i, digit in enumerate(s_value):
            self.screen.blit(self.header_digits[int(digit)], (x + i * 19, y))

    def draw_end_screen(self, status, current_time, best_time):
        """
        Відображає вікно кінця гри (перемога або поразка).
    
        Args:
            status (str): "win" або "lose" для визначення типу кінцевого екрану.
            current_time (int): Час, витрачений на поточну гру.
            best_time (int): Найкращий час сесії для поточного рівня складності.
        """
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        
        # Затемнення поля
        self.screen.blit(self.overlay, (0, 0))
        
        # Визначаємо індекс кадру (кожні 500 мс)
        frame_idx = (pygame.time.get_ticks() // 500) % 2
        
        # Малюємо базове вікно
        win_img = self.endscreen_frames[frame_idx]
        win_x = (sw - win_img.get_width()) // 2
        win_y = (sh - win_img.get_height()) // 2
        self.screen.blit(win_img, (win_x, win_y))
        
        # Малюємо іконки для поточного та найкращого часу
        self.screen.blit(self.trophy_frames[frame_idx], (win_x, win_y))
        self.screen.blit(self.icon_clock[frame_idx], (win_x + 40, win_y + 65))
        
        # Малюємо череп (при програші)
        if status == 'lose':
            self.screen.blit(self.skull_frames[frame_idx], (win_x, win_y))
        # Малюємо усміхнене личко (при перемозі)
        else:
             self.screen.blit(self.smiley_frames[frame_idx], (win_x, win_y))
        
        # Малюємо цифри
        # Поточний результат
        self.draw_header_number(current_time, win_x + 20, win_y + 110)
        
        # Найкращий результат сесії
        self.draw_header_number(best_time, win_x + 180, win_y + 110)

        # кнопка RESTART
        mouse_pos = pygame.mouse.get_pos()
        # Розраховуємо позицію кнопки
        self.btn_rect = pygame.Rect(win_x+110, win_y+110, 75, 50)
        
        # Перевірка: чи наведена миша на кнопку
        if self.btn_rect.collidepoint(mouse_pos):
            btn_img = self.restart_btn_frames[1]
            draw_x = self.btn_rect.x-10
            draw_y = self.btn_rect.y
        else:
            btn_img = self.restart_btn_frames[0]
            draw_x = self.btn_rect.x-2
            draw_y = self.btn_rect.y
            
        self.screen.blit(btn_img, (draw_x, draw_y))

    def is_restart_clicked(self, pos):
        """ 
        Перевіряє, чи клік був по кнопці рестарту.

        Args:
            pos (tuple): Кортеж (x, y) з координатами кліку миші.
        Returns:
            bool: True, якщо клік був по кнопці
        """
        return hasattr(self, 'btn_rect') and self.btn_rect.collidepoint(pos)
    
    def draw_difficulty_menu(self):
        """
          Відображає випадаюче меню вибору складності.
        """
        mouse_pos = pygame.mouse.get_pos()
        frame_idx = (pygame.time.get_ticks() // 400) % 2

        # Позиція плашки меню
        menu_x, menu_y = 10, 16 
        self.screen.blit(self.drop_menu_frames[frame_idx], (menu_x, menu_y))

        options = list(DIFFICULTIES.keys())
        self.menu_rects = {}
        
        start_y_offset = 31  
        line_spacing = 35 

        for i, opt in enumerate(options):
            opt_y = menu_y + start_y_offset + (i * line_spacing)
            
            # Зона кліку
            rect = pygame.Rect(menu_x, opt_y, 120, line_spacing)
            self.menu_rects[opt] = rect

            # Ефект наведення
            if rect.collidepoint(mouse_pos):
                # Малюємо виділення
                self.screen.blit(self.selected_menu, (rect.x, rect.y-5))

            self.screen.blit(self.diff_labels[opt], (rect.x + 5, rect.y))