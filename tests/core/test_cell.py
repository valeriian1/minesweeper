import pytest
from src.core.cell import Cell

pytestmark = pytest.mark.core


@pytest.fixture
def basic_cell():
    return Cell(col=0, row=0)


@pytest.mark.parametrize("col, row", [
    (0, 0),
    (5, 3),
    (10, 15)
])
def test_cell_initialization(col, row):
    cell = Cell(col=col, row=row)
    assert cell.col == col
    assert cell.row == row
    assert not cell.is_mine
    assert not cell.is_open
    assert not cell.is_flagged
    assert cell.adjacent_mines == 0


def test_toggle_flag(basic_cell):
    basic_cell.toggle_flag()
    assert basic_cell.is_flagged is True

    basic_cell.toggle_flag()
    assert basic_cell.is_flagged is False


def test_toggle_flag_when_open(basic_cell):
    basic_cell.is_open = True
    basic_cell.toggle_flag()
    assert basic_cell.is_flagged is False


def test_reveal(basic_cell):
    result = basic_cell.reveal()
    assert result is True
    assert basic_cell.is_open is True


def test_reveal_already_open(basic_cell):
    basic_cell.is_open = True
    result = basic_cell.reveal()
    assert result is False


def test_reveal_flagged(basic_cell):
    basic_cell.toggle_flag()
    result = basic_cell.reveal()
    assert result is False
    assert basic_cell.is_open is False
