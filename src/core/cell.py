
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_open = False
        self.is_flagged = False
        self.adjacent_mines = 0



