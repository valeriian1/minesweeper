import pytest
from unittest.mock import patch
from src.core.board import Board
from src.core.cell import Cell

pytestmark = pytest.mark.core


@pytest.fixture
def board_10x10():
    return Board(rows=10, cols=10, mines_count=10)


@pytest.fixture
def empty_board_3x3():
    return Board(rows=3, cols=3, mines_count=0)


@pytest.mark.parametrize("rows, cols, mines", [
    (10, 15, 20),
    (5, 5, 5),
    (20, 20, 50)
])
def test_board_initialization(rows, cols, mines):
    board = Board(rows=rows, cols=cols, mines_count=mines)
    assert board.rows == rows
    assert board.cols == cols
    assert board.mines_count == mines
    assert len(board.grid) == rows
    assert len(board.grid[0]) == cols
    assert isinstance(board.grid[0][0], Cell)


def test_get_neighbors():
    board = Board(rows=5, cols=5, mines_count=5)

    # Middle cell
    neighbors_middle = board._get_neighbors(2, 2)
    assert len(neighbors_middle) == 8
    expected_middle = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 3),
        (3, 1), (3, 2), (3, 3)
    ]
    for n in expected_middle:
        assert n in neighbors_middle

    # Corner cell (top-left)
    neighbors_corner = board._get_neighbors(0, 0)
    assert len(neighbors_corner) == 3
    expected_corner = [(0, 1), (1, 0), (1, 1)]
    for n in expected_corner:
        assert n in neighbors_corner


def test_place_mines(board_10x10):
    board_10x10.place_mines(safe_row=5, safe_col=5)

    mines_placed = sum(
        cell.is_mine for row in board_10x10.grid for cell in row
    )
    assert mines_placed == 10

    # Check safe zone: 3x3 area around (5,5) should not have mines
    for row in range(4, 7):
        for col in range(4, 7):
            assert not board_10x10.grid[row][col].is_mine


@patch('src.core.board.random.randint')
def test_place_mines_deterministic(mock_randint):
    board = Board(rows=5, cols=5, mines_count=2)

    # The function calls col = random.randint(0, cols - 1)
    # then row = random.randint(0, rows - 1)
    # We provide values: (col=0, row=0) then (col=4, row=4)
    mock_randint.side_effect = [0, 0, 4, 4]

    board.place_mines(safe_row=2, safe_col=2)

    assert board.grid[0][0].is_mine is True
    assert board.grid[4][4].is_mine is True
    assert sum(cell.is_mine for row in board.grid for cell in row) == 2


def test_calculate_neighbors(empty_board_3x3):
    empty_board_3x3.grid[1][1].is_mine = True
    empty_board_3x3.calculate_neighbors()

    assert empty_board_3x3.grid[0][0].adjacent_mines == 1
    assert empty_board_3x3.grid[0][1].adjacent_mines == 1
    assert empty_board_3x3.grid[0][2].adjacent_mines == 1
    assert empty_board_3x3.grid[1][0].adjacent_mines == 1
    assert empty_board_3x3.grid[1][2].adjacent_mines == 1
    assert empty_board_3x3.grid[2][0].adjacent_mines == 1
    assert empty_board_3x3.grid[2][1].adjacent_mines == 1
    assert empty_board_3x3.grid[2][2].adjacent_mines == 1


def test_count_adjacent_mines(empty_board_3x3):
    empty_board_3x3.grid[0][0].is_mine = True
    empty_board_3x3.grid[0][1].is_mine = True

    cell = empty_board_3x3.grid[1][0]
    count = empty_board_3x3._count_adjacent_mines(cell)
    assert count == 2


def test_flood_fill(empty_board_3x3):
    empty_board_3x3.flood_fill(1, 1)

    # Whole board should be revealed since there are 0 mines
    for row in empty_board_3x3.grid:
        for cell in row:
            assert cell.is_open is True


def test_reveal_all_mines(empty_board_3x3):
    empty_board_3x3.grid[0][0].is_mine = True
    empty_board_3x3.grid[1][1].is_mine = True

    # Flag one mine, the other should be revealed
    empty_board_3x3.grid[1][1].toggle_flag()

    empty_board_3x3.reveal_all_mines()

    assert empty_board_3x3.grid[0][0].is_open is True
    assert empty_board_3x3.grid[1][1].is_open is False
    assert empty_board_3x3.grid[0][1].is_open is False


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
