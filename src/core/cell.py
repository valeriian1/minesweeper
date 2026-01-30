
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_open = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def toggle_flag(self):
        if not self.is_open:
            self.is_flagged = not self.is_flagged

    def reveal(self):
        if self.is_flagged or self.is_open:
            return False
        self.is_open = True
        return True



