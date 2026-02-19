import random
from src.core.cell import Cell


class Board:
    def __init__(self, rows: int, cols: int, mines_count: int):
        """
        Ініціалізує ігрове поле.

        Args:
            rows: Кількість рядків на полі.
            cols: Кількість стовпців на полі.
            mines_count: Загальна кількість мін для розміщення.
        """
        self.rows = rows
        self.cols = cols
        self.mines_count = mines_count
        self.grid = self._create_grid()


    def _create_grid(self) -> list[list[Cell]]:
        grid = []
        for row in range(self.rows):
            line = []
            for col in range(self.cols):
                line.append(Cell(col, row))
            grid.append(line)
        return grid

    def _get_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        neighbors = []
        for delta_row in range(-1, 2):
            for delta_col in range(-1, 2):
                if delta_row == 0 and delta_col == 0:
                    continue
                neighbor_row = row + delta_row
                neighbor_col = col + delta_col
                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                    neighbors.append((neighbor_row, neighbor_col))
        return neighbors

    def place_mines(self, safe_row, safe_col) -> None:
        """
        Випадково розміщує міни на полі, уникаючи безпечної зони навколо першого кліку.

        Args:
            safe_row: Рядок першого кліку.
            safe_col: Стовпець першого кліку.
        """

        mines_placed = 0
        while mines_placed < self.mines_count:
            col = random.randint(0, self.cols - 1)
            row = random.randint(0, self.rows - 1)

            if abs(row - safe_row) <= 1 and abs(col - safe_col) <= 1:
                continue

            cell = self.grid[row][col]
            if not cell.is_mine:
                cell.is_mine = True
                mines_placed += 1

    def calculate_neighbors(self) -> None:
        """
        Обчислює кількість сусідніх мін для всіх комірок без мін.
        """
        for row in self.grid:
            for cell in row:
                if not cell.is_mine:
                    cell.adjacent_mines = self._count_adjacent_mines(cell)

    def _count_adjacent_mines(self, cell: Cell) -> int:

        count = 0
        for neighbor_row, neighbor_col in self._get_neighbors(cell.row, cell.col):
            if self.grid[neighbor_row][neighbor_col].is_mine:
                count += 1
        return count

    def flood_fill(self, row: int, col: int) -> None:
        """
        Ітеративно відкриває порожні комірки, починаючи з вказаних координат.

        Args:
            row: Рядок, з якого починати.
            col: Стовпець, з якого починати.
        """
        stack = [(row, col)]

        while stack:
            current_row, current_col = stack.pop()
            current_cell = self.grid[current_row][current_col]

            if current_cell.reveal() and current_cell.adjacent_mines == 0:
                for neighbor_row, neighbor_col in self._get_neighbors(current_row, current_col):
                    stack.append((neighbor_row, neighbor_col))

    def reveal_all_mines(self) -> None:
        """Відкриває всі непозначені прапорцем міни на полі."""
        for row in self.grid:
            for cell in row:
                if cell.is_mine and not cell.is_open and not cell.is_flagged:
                    cell.is_open = True

    def check_win(self) -> bool:
        """Перевіряє, чи гравець виграв гру."""
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_open:
                    return False
        return True

    def get_mines_remaining(self) -> int:
        """Повертає кількість мін, що залишилися (міни мінус прапорці)."""
        flags_count = 0
        for row in self.grid:
            for cell in row:
                if cell.is_flagged:
                    flags_count += 1
        return self.mines_count - flags_count