import pygame
import sys
import time
from src.core.board import Board
from src.ui.renderer import GameRenderer
from src.utils.constants import DIFFICULTIES, HEADER_HEIGHT, BG_COLOR

class Game:
    def __init__(self):
        """
        Ініціалізація гри
        Встановлює початкові параметри Pygame, завантажує список складностей,
        запускає початкове налаштування вікна
        """
        pygame.init()
        
        # Створюємо список ключів Easy, Medium, Hard, для зручного перемикання
        self.difficulty_names = list(DIFFICULTIES.keys())
        self.current_diff_idx = 0
        self.difficulty = self.difficulty_names[self.current_diff_idx]
        
        self.running = True
        self.setup_game()

    def setup_game(self):
        """
        Конфігурація ігрового сеансу
        Викликається при старті гри, зміні складності або рестарті
        Створює об'єкти поля та візуалізатора
        """
        config = DIFFICULTIES[self.difficulty]
        self.rows, self.cols = config["rows"], config["cols"]
        self.mines_count, self.cell_size = config["mines"], config["cell_size"]
        
        width = self.cols * self.cell_size
        height = (self.rows * self.cell_size) + HEADER_HEIGHT
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Minesweeper")
        
        self.board = Board(self.rows, self.cols, self.mines_count)
        self.renderer = GameRenderer(self.screen, self.cell_size, HEADER_HEIGHT)
        
        # Ігрові стани
        self.first_click = True  
        self.game_over = False   
        self.won = False        
        self.start_time = 0     
        self.elapsed_time = 0    

    def handle_events(self):
        """
        Обробка черги подій Pygame
        Слухає системні сигнали та дії користувача
        """
        for event in pygame.event.get():
            # Закриття вікна через хрестик
            if event.type == pygame.QUIT:
                self.running = False
            
            # Обробка натискань клавіш миші
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

    def _handle_mouse_click(self, event):
        """
        Розподіляє кліки миші між ігровими зонами
        Якщо гра закінчена, будь-який клік скидає гру до початку
        """
        if self.game_over or self.won:
            self.setup_game() 
            return

        pos = pygame.mouse.get_pos() # Отримуємо координати курсора
        
        # Перевіряємо, чи клік був у верхній панелі чи на полі
        if pos[1] < HEADER_HEIGHT:
            self._handle_header_click(pos)
        else:
            # Передаємо координати та номер кнопки 
            self._handle_board_click(pos, event.button)

    def _handle_header_click(self, pos):
        """
        Обробка взаємодії з верхнім меню
        Зараз реалізовано зміну складності при натисканні в лівій частині хедера
        """
        if 10 <= pos[0] <= 110: 
            self.current_diff_idx = (self.current_diff_idx + 1) % len(self.difficulty_names)
            self.difficulty = self.difficulty_names[self.current_diff_idx]
            self.setup_game()

    def _handle_board_click(self, pos, mouse_button):
        """
        Перетворює координати пікселів у координати сітки 
        та виконує відповідну ігрову дію
        """
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
        """
        Логіка відкриття клітинки
        Враховує правила першого ходу, підриву на міні та ланцюгового відкриття
        """
        # Не дозволяємо відкривати клітинки з прапорцями
        if cell.is_flagged:
            return

        # Перший клік у грі: генеруємо міни так, щоб гравець не програв одразу
        if self.first_click:
            self._start_game_logic(x, y) 

        if cell.is_mine:
            # Кінець гри: показуємо всі міни на полі
            self.game_over = True
            self.board.reveal_all_mines()
        else:
            # Якщо міни немає, відкриваємо порожнечу 
            self.board.flood_fill(x, y)
            # Після кожного ходу перевіряємо, чи не залишилися тільки міни 
            if self.board.check_win():
                self.won = True

    def _start_game_logic(self, start_x, start_y):
        """
        Відкладена ініціалізація
        Міни створюються тільки тоді, коли гравець вперше клікнув на поле
        """
        # Передаємо координати першого кліку як безпечну зону
        self.board.place_mines(safe_x=start_x, safe_y=start_y)
        # Розраховуємо кількість мін навколо для кожної клітинки
        self.board.calculate_neighbors()
        self.first_click = False
        self.start_time = time.time()

    def update(self):
        """
        Оновлення стану гри в реальному часі
        Викликається кожного кадру перед малюванням
        """
        if not self.first_click and not self.game_over and not self.won:
            self.elapsed_time = int(time.time() - self.start_time)

    def draw(self):
        """
        Візуалізація гри 
        Використовує Renderer для малювання шарів
        """
        self.screen.fill(BG_COLOR) 
        
        # Малюємо сітку та стан клітинок
        self.renderer.draw_board(self.board)
        
        # Малюємо верхню панель 
        self.renderer.draw_header(
            self.board.get_mines_remaining(), 
            self.elapsed_time, 
            self.difficulty
        )
        
        # Виводимо підготовлений кадр на монітор
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