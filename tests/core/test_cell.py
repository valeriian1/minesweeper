import pytest
from src.core.cell import Cell


def test_cell_initialization():
    cell = Cell(col=5, row=3)
    assert cell.col == 5
    assert cell.row == 3
    assert not cell.is_mine
    assert not cell.is_open
    assert not cell.is_flagged
    assert cell.adjacent_mines == 0


def test_toggle_flag():
    cell = Cell(col=0, row=0)
    
    # Initial toggle (flag)
    cell.toggle_flag()
    assert cell.is_flagged is True
    
    # Second toggle (unflag)
    cell.toggle_flag()
    assert cell.is_flagged is False


def test_toggle_flag_when_open():
    cell = Cell(col=0, row=0)
    cell.is_open = True
    
    cell.toggle_flag()
    assert cell.is_flagged is False  # Cannot flag an opened cell


def test_reveal():
    cell = Cell(col=0, row=0)
    result = cell.reveal()
    
    assert result is True
    assert cell.is_open is True


def test_reveal_already_open():
    cell = Cell(col=0, row=0)
    cell.is_open = True
    
    result = cell.reveal()
    assert result is False


def test_reveal_flagged():
    cell = Cell(col=0, row=0)
    cell.toggle_flag()
    
    result = cell.reveal()
    assert result is False
    assert cell.is_open is False
