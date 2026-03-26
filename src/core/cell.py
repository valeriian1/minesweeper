class Cell:
    def __init__(self, col: int, row: int):
        """
        Ініціалізує комірку з координатами на сітці.

        Args:
            col: Індекс стовпця.
            row: Індекс рядка.
        """
        self.col = col
        self.row = row
        self.is_mine: bool = False
        self.is_open: bool = False
        self.is_flagged: bool = False
        self.adjacent_mines: int = 0

    def toggle_flag(self) -> None:
        """
        Перемикає стан прапорця комірки, якщо вона не відкрита.
        """
        if not self.is_open:
            self.is_flagged = not self.is_flagged

    def reveal(self) -> bool:
        """
        Відкриває комірку, якщо вона не позначена прапорцем
        і ще не відкрита.

        Returns:
            True, якщо комірку було успішно відкрито, False — якщо вона
            вже відкрита або позначена.
        """
        if self.is_flagged or self.is_open:
            return False
        self.is_open = True
        return True
