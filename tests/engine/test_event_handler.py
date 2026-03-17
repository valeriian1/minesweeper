import pytest
import pygame
from unittest.mock import MagicMock, patch
from src.utils.constants import HEADER_HEIGHT

class TestEventHandler:

    def test_open_cell_status_change(self, game_easy):
        """
        Перевірка зміни статусу клітинки на «відкрита».
        """
        # Force a mine layout to be deterministic
        game_easy.board.place_mines(safe_row=0, safe_col=0)
        cell = game_easy.board.grid[0][0]
        
        assert cell.is_open is False
        
        # First click happens here
        game_easy.event_handler._open_cell(0, 0)
        
        # Cell should be open
        assert cell.is_open is True

    def test_open_cell_game_over_on_mine(self, game_easy):
        """
        Перевірка чи зупиняється гра (self.game_over = True), якщо гравець наступив на міну.
        """
        # Since first click is safe, we simulate the first click to setup the board
        game_easy.event_handler._open_cell(0, 0)
        
        # Find a mine
        mine_row, mine_col = None, None
        for r in range(game_easy.rows):
            for c in range(game_easy.cols):
                if game_easy.board.grid[r][c].is_mine:
                    mine_row, mine_col = r, c
                    break
            if mine_row is not None:
                break
                
        # Make sure game is not over
        assert game_easy.game_over is False
        
        # Click the mine
        game_easy.event_handler._open_cell(mine_row, mine_col)
        
        # Game should be over and that cell should be open
        assert game_easy.game_over is True
        assert game_easy.board.grid[mine_row][mine_col].is_mine is True

    def test_open_cell_flood_fill(self, mock_pygame):
        """
        Перевірка чи працює рекурсивне відкриття порожніх клітинок (Flood Fill).
        """
        from src.engine.game import Game
        game = Game(difficulty="easy")
        board = game.board
        
        # Create a deterministic board layout (mock place_mines and calculate_neighbors to do nothing)
        # We will manually set the mines
        # 0 0 0
        # 0 M 0
        # 0 0 0
        # clicking 0,0 should not flood fill to the right side if we put mines surrounding it,
        # let's do a simple 3x3 no mine area, and place a line of mines to block flood fill
        
        def fake_generate(row, col):
            game.first_click = False
            
            # Place mines in an L shape blocking (0,0) from (2,2)
            board.grid[0][1].is_mine = True
            board.grid[1][1].is_mine = True
            board.grid[1][0].is_mine = True
            
            board.calculate_neighbors()
            
        game.event_handler._generate_board_after_first_click = fake_generate
        
        # Click (0,0) - should open, but NOT propagate past the mines
        game.event_handler._open_cell(0, 0)
        
        assert board.grid[0][0].is_open is True
        assert board.grid[2][2].is_open is False  # Safe cell blocked by L-shape mines

    def test_handle_mouse_click_conversion(self, game_easy):
        """
        Перевірка перетворення координат кліку миші.
        """
        # Set up a mock for get_cell_from_pos from renderer
        # renderer translates (x, y) into (row, col)
        # We simulate a click by mocking renderer.get_cell_from_pos
        mock_event = MagicMock()
        mock_event.button = 1 # Left click
        
        # Coordinates (x=100, y=100 + HEADER_HEIGHT) -> cell
        pos = (100, 100 + HEADER_HEIGHT)
        game_easy.renderer.get_cell_from_pos = MagicMock(return_value=(2, 2))
        game_easy.event_handler._open_cell = MagicMock()
        
        with patch("pygame.mouse.get_pos", return_value=pos):
            game_easy.event_handler._handle_mouse_click(mock_event)
            
        # Ensure it properly handled the grid interaction and called _open_cell
        game_easy.renderer.get_cell_from_pos.assert_called_once_with(pos)
        game_easy.event_handler._open_cell.assert_called_once_with(2, 2)

    def test_handle_mouse_click_ignore_header(self, game_easy):
        """
        Ігнорування кліків у зоні хедеру (не враховуючи кнопку меню).
        """
        mock_event = MagicMock()
        mock_event.button = 1
        
        pos = (200, HEADER_HEIGHT - 10) # In the header
        
        game_easy.event_handler._handle_grid_interaction = MagicMock()
        
        with patch("pygame.mouse.get_pos", return_value=pos):
            game_easy.event_handler._handle_mouse_click(mock_event)
            
        # _handle_grid_interaction should not be called
        game_easy.event_handler._handle_grid_interaction.assert_not_called()

    def test_handle_events_quit(self, game_easy):
        """
        Тестування закриття вікна (подія pygame.QUIT).
        """
        # Create a mock event of type pygame.QUIT
        quit_event = MagicMock()
        quit_event.type = pygame.QUIT
        
        # Patch pygame.event.get to return our mock event
        with patch("pygame.event.get", return_value=[quit_event]):
            game_easy.event_handler.handle_events()
            
        # game.running should become False
        assert game_easy.running is False
