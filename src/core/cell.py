
class Cell:
    def __init__(self, x, y):
        """
        Initialize a Cell with its grid coordinates.

        Args:
            x (int): The x-coordinate (column).
            y (int): The y-coordinate (row).
        """
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_open = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def toggle_flag(self):
        """
        Toggles the flagged state of the cell if it is not open.
        """
        if not self.is_open:
            self.is_flagged = not self.is_flagged

    def reveal(self):
        """
        Reveals the cell if it is not flagged or already open.

        Returns:
            bool: True if the cell was successfully opened, False if it was already open or flagged.
        """
        if self.is_flagged or self.is_open:
            return False
        self.is_open = True
        return True



