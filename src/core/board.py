import random
from src.core.cell import Cell


class Board:
    def __init__(self, rows: int, cols: int, mines_count: int):
        """
        Initialize the game board.

        Args:
            rows: The number of rows on the board.
            cols: The number of columns on the board.
            mines_count: The total number of mines to place.
        """
        self.rows = rows
        self.cols = cols
        self.mines_count = mines_count
        self.grid = self._create_grid()

    def __getitem__(self, pos: tuple[int, int]) -> Cell:
        """
        Get the cell at the specified position.

        Args:
            pos: A tuple containing the (row, col) coordinates.

        Returns:
            The cell object at the specified coordinates.
        """
        row, col = pos
        return self.grid[row][col]

    def _create_grid(self) -> list[list[Cell]]:
        """
        Create the 2D grid of Cell objects.

        Returns:
            A 2D list of Cell objects representing the board.
        """
        return [[Cell(col, row) for col in range(self.cols)] for row in range(self.rows)]

    def _get_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        """
        Get valid neighboring coordinates for the given cell position.

        Args:
            row: The row of the target cell.
            col: The column of the target cell.

        Returns:
            A list of (row, col) tuples of valid neighbor positions.
        """
        neighbors = []
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors.append((nr, nc))
        return neighbors

    def place_mines(self, safe_row: int | None = None, safe_col: int | None = None) -> None:
        """
        Randomly place mines on the board, avoiding the safe zone around the first click.

        Args:
            safe_row: The row of the safe zone (first click).
            safe_col: The column of the safe zone (first click).

        Raises:
            ValueError: If mines_count exceeds the number of available cells.
        """
        total_cells = self.rows * self.cols
        safe_zone_size = 9 if (safe_row is not None and safe_col is not None) else 0
        available_cells = total_cells - safe_zone_size

        if self.mines_count > available_cells:
            raise ValueError(
                f"Cannot place {self.mines_count} mines: only {available_cells} cells available."
            )

        mines_placed = 0
        while mines_placed < self.mines_count:
            col = random.randint(0, self.cols - 1)
            row = random.randint(0, self.rows - 1)

            if safe_row is not None and safe_col is not None:
                if abs(row - safe_row) <= 1 and abs(col - safe_col) <= 1:
                    continue

            cell = self.grid[row][col]
            if not cell.is_mine:
                cell.is_mine = True
                mines_placed += 1

    def calculate_neighbors(self) -> None:
        """
        Calculate adjacent mine counts for all non-mine cells.
        """
        for row in self.grid:
            for cell in row:
                if not cell.is_mine:
                    cell.adjacent_mines = self._count_adjacent_mines(cell)

    def _count_adjacent_mines(self, cell: Cell) -> int:
        """
        Count the number of mines in the 8 neighboring cells.

        Args:
            cell: The target cell to check.

        Returns:
            The number of adjacent mines.
        """
        return sum(
            self.grid[nr][nc].is_mine
            for nr, nc in self._get_neighbors(cell.row, cell.col)
        )

    def flood_fill(self, row: int, col: int) -> None:
        """
        Iteratively reveal empty cells starting from the given coordinates.

        Args:
            row: The row to start from.
            col: The column to start from.
        """
        stack = [(row, col)]

        while stack:
            r, c = stack.pop()

            if not (0 <= r < self.rows and 0 <= c < self.cols):
                continue

            current_cell = self.grid[r][c]

            if not current_cell.reveal():
                continue

            if current_cell.adjacent_mines == 0:
                for nr, nc in self._get_neighbors(r, c):
                    stack.append((nr, nc))

    def reveal_all_mines(self) -> list[Cell]:
        """
        Reveal all unflagged mines on the board.

        Returns:
            A list of revealed mine cells.
        """
        mines_list = []
        for row in self.grid:
            for cell in row:
                if cell.is_mine and not cell.is_open and not cell.is_flagged:
                    cell.is_open = True
                    mines_list.append(cell)
        return mines_list

    def check_win(self) -> bool:
        """
        Check if the player has won the game.

        Returns:
            True if all non-mine cells are open, False otherwise.
        """
        return all(cell.is_mine or cell.is_open for row in self.grid for cell in row)

    def get_mines_remaining(self) -> int:
        """
        Get the estimated number of remaining mines based on placed flags.

        Returns:
            The number of mines minus the number of flags placed.
        """
        flags_count = sum(cell.is_flagged for row in self.grid for cell in row)
        return self.mines_count - flags_count