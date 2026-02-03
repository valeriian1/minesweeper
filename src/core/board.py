import random
from cell import Cell

class Board:
   def __init__(self, rows, cols, mines_count):
       self.rows = rows
       self.cols = cols
       self.mines_count = mines_count
       self.grid = self._create_grid()

   def __getitem__(self, pos):
       x, y = pos
       return self.grid[y][x]

   def _create_grid(self):
       grid = []
       for i in range(0, self.rows):
           row = []
           for j in range(0, self.cols):
               new_cell = Cell(j, i)
               row.append(new_cell)
           grid.append(row)
       return grid

   def place_mines(self, safe_x=None, safe_y=None):
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
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    continue
                cell.adjacent_mines = self._count_adjacent_mines(cell)

   def _count_adjacent_mines(self, cell):
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
       mines_list = []
       for row in self.grid:
           for cell in row:
               if cell.is_mine and not cell.is_open and not cell.is_flagged:
                   cell.is_open = True
                   mines_list.append(cell)
       return mines_list

   def check_win(self):
       for row in self.grid:
           for cell in row:
               if not cell.is_mine and not cell.is_open:
                   return False
       return True

   def get_mines_remaining(self):
       flags_count = 0
       for row in self.grid:
           for cell in row:
               if cell.is_flagged:
                   flags_count += 1

       return self.mines_count - flags_count