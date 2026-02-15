import random
from src.core.cell import Cell

class Board:
   def __init__(self, rows, cols, mines_count):
       """
       Initialize the game board.

       Args:
           rows (int): The number of rows on the board.
           cols (int): The number of columns on the board.
           mines_count (int): The total number of mines to place.
       """
       self.rows = rows
       self.cols = cols
       self.mines_count = mines_count
       self.grid = self._create_grid()

   def __getitem__(self, pos):
       """
       Get the cell at the specified position.

       Args:
           pos (tuple): A tuple containing the (x, y) coordinates.

       Returns:
           Cell: The cell object at the specified coordinates.
       """
       x, y = pos
       return self.grid[y][x]

   def _create_grid(self):
       """
       Create the 2D grid of Cell objects.

       Returns:
           list: A 2D list of Cell objects representing the board.
       """
       grid = []
       for i in range(0, self.rows):
           row = []
           for j in range(0, self.cols):
               new_cell = Cell(j, i)
               row.append(new_cell)
           grid.append(row)
       return grid

   def place_mines(self, safe_x=None, safe_y=None):
       """
       Randomly place mines on the board, avoiding the safe zone.

       Args:
           safe_x (int, optional): The x-coordinate of the safe zone (first click).
           safe_y (int, optional): The y-coordinate of the safe zone (first click).
       """
       mines_placed = 0
       while mines_placed < self.mines_count:
           x = random.randint(0, self.cols - 1)
           y = random.randint(0, self.rows - 1)

           if safe_x is not None and safe_y is not None:
               if abs(x - safe_x) <= 1 and abs(y - safe_y) <= 1:
                   continue

           cell = self.grid[y][x]
           if not cell.is_mine:
               cell.is_mine = True
               mines_placed += 1

   def calculate_neighbors(self):
        """
        Calculate adjacent mine counts for all non-mine cells.
        """
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    continue
                cell.adjacent_mines = self._count_adjacent_mines(cell)

   def _count_adjacent_mines(self, cell):
        """
        Count the number of mines in the 8 neighboring cells.

        Args:
            cell (Cell): The target cell to check.

        Returns:
            int: The number of adjacent mines.
        """
        count = 0

        for i in range(-1, 2):
            for j in range(-1, 2):

                if i == 0 and j == 0:
                    continue

                neighbor_x = cell.x + i
                neighbor_y = cell.y + j

                if 0 <= neighbor_x < self.cols and 0 <= neighbor_y < self.rows:
                    if self.grid[neighbor_y][neighbor_x].is_mine:
                        count += 1
        return count

   def flood_fill(self, x, y):
       """
       Recursively reveal empty cells starting from the given coordinates.

       Args:
           x (int): The x-coordinate to start from.
           y (int): The y-coordinate to start from.
       """
       if not (0 <= x < self.cols and  0 <= y < self.rows):
           return

       current_cell = self.grid[y][x]

       if current_cell.is_open or current_cell.is_mine or current_cell.is_flagged:
           return

       current_cell.is_open = True

       if current_cell.adjacent_mines == 0:
           for i in range(-1, 2):
               for j in range(-1, 2):
                   if i == 0 and j == 0:
                       continue

                   self.flood_fill(x + i, y + j)

   def reveal_all_mines(self):
       """
       Reveal all unflagged mines on the board.

       Returns:
           list: A list of revealed mine cells.
       """
       mines_list = []
       for row in self.grid:
           for cell in row:
               if cell.is_mine and not cell.is_open and not cell.is_flagged:
                   cell.is_open = True
                   mines_list.append(cell)
       return mines_list

   def check_win(self):
       """
       Check if the player has won the game.

       Returns:
           bool: True if all non-mine cells are open, False otherwise.
       """
       for row in self.grid:
           for cell in row:
               if not cell.is_mine and not cell.is_open:
                   return False
       return True

   def get_mines_remaining(self):
       """
       Get the estimated number of remaining mines based on placed flags.

       Returns:
           int: The number of mines minus the number of flags placed.
       """
       flags_count = 0
       for row in self.grid:
           for cell in row:
               if cell.is_flagged:
                   flags_count += 1

       return self.mines_count - flags_count