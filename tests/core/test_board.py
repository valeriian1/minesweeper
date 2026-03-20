import pytest
from src.core.board import Board
from src.core.cell import Cell


def test_board_initialization():
    board = Board(rows=10, cols=15, mines_count=20)
    assert board.rows == 10
    assert board.cols == 15
    assert board.mines_count == 20
    assert len(board.grid) == 10
    assert len(board.grid[0]) == 15
    assert isinstance(board.grid[0][0], Cell)


def test_get_neighbors():
    board = Board(rows=5, cols=5, mines_count=5)
    
    # Middle cell
    neighbors_middle = board._get_neighbors(2, 2)
    assert len(neighbors_middle) == 8
    expected_middle = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]
    for n in expected_middle:
        assert n in neighbors_middle

    # Corner cell (top-left)
    neighbors_corner = board._get_neighbors(0, 0)
    assert len(neighbors_corner) == 3
    expected_corner = [(0, 1), (1, 0), (1, 1)]
    for n in expected_corner:
        assert n in neighbors_corner


def test_place_mines():
    board = Board(rows=10, cols=10, mines_count=10)
    board.place_mines(safe_row=5, safe_col=5)
    
    mines_placed = sum(cell.is_mine for row in board.grid for cell in row)
    assert mines_placed == 10
    
    # Check safe zone: 3x3 area around (5,5) should not have mines
    for row in range(4, 7):
        for col in range(4, 7):
            assert not board.grid[row][col].is_mine


def test_calculate_neighbors():
    board = Board(rows=3, cols=3, mines_count=0)
    board.grid[1][1].is_mine = True
    board.calculate_neighbors()
    
    assert board.grid[0][0].adjacent_mines == 1
    assert board.grid[0][1].adjacent_mines == 1
    assert board.grid[0][2].adjacent_mines == 1
    assert board.grid[1][0].adjacent_mines == 1
    assert board.grid[1][2].adjacent_mines == 1
    assert board.grid[2][0].adjacent_mines == 1
    assert board.grid[2][1].adjacent_mines == 1
    assert board.grid[2][2].adjacent_mines == 1


def test_count_adjacent_mines():
    board = Board(rows=3, cols=3, mines_count=0)
    board.grid[0][0].is_mine = True
    board.grid[0][1].is_mine = True
    
    cell = board.grid[1][0]
    count = board._count_adjacent_mines(cell)
    assert count == 2


def test_flood_fill():
    board = Board(rows=3, cols=3, mines_count=0)
    board.flood_fill(1, 1)
    
    # Whole board should be revealed since there are 0 mines
    for row in board.grid:
        for cell in row:
            assert cell.is_open is True


def test_reveal_all_mines():
    board = Board(rows=3, cols=3, mines_count=0)
    board.grid[0][0].is_mine = True
    board.grid[1][1].is_mine = True
    
    # Flag one mine, the other should be revealed
    board.grid[1][1].toggle_flag()
    
    board.reveal_all_mines()
    
    assert board.grid[0][0].is_open is True
    assert board.grid[1][1].is_open is False  # Flagged mines shouldn't be opened
    assert board.grid[0][1].is_open is False  # Empty cells shouldn't be opened


def test_check_win():
    board = Board(rows=2, cols=2, mines_count=1)
    # Put mine at (0,0)
    board.grid[0][0].is_mine = True
    # Initial state
    assert board.check_win() is False
    
    # Open all non-mine cells
    board.grid[0][1].reveal()
    board.grid[1][0].reveal()
    board.grid[1][1].reveal()
    
    assert board.check_win() is True


def test_get_mines_remaining():
    board = Board(rows=5, cols=5, mines_count=10)
    board.grid[0][0].toggle_flag()
    board.grid[1][1].toggle_flag()
    board.grid[2][2].toggle_flag()
    
    remaining = board.get_mines_remaining()
    assert remaining == 7
