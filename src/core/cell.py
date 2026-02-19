class Cell:
    def __init__(self, col: int, row: int):
        """
        Initialize a Cell with its grid coordinates.

        Args:
            col: The column index.
            row: The row index.
        """
        self.col = col
        self.row = row
        self.is_mine: bool = False
        self.is_open: bool = False
        self.is_flagged: bool = False
        self.adjacent_mines: int = 0

    def toggle_flag(self) -> None:
        """
        Toggles the flagged state of the cell if it is not open.
        """
        if not self.is_open:
            self.is_flagged = not self.is_flagged

    def reveal(self) -> bool:
        """
        Reveals the cell if it is not flagged or already open.

        Returns:
            True if the cell was successfully opened, False if it was already open or flagged.
        """
        if self.is_flagged or self.is_open:
            return False
        self.is_open = True
        return True
