from random import random

from cell import Cell

class Board:
   def __init__(self, rows, cols, mines_count):
       self.rows = rows
       self.cols = cols
       self.mines_count = mines_count

   def _create_grid(self):
       grid = []
       for i in range(0, self.rows):
           row = []
           for j in range(0, self.cols):
               new_cell = Cell(j, i)
               row.append(new_cell)
           grid.append(row)
       return grid

   def place_mines(self):
       mines_placed = 0
       while mines_placed < self.mines_count:
           x = random.randint(0, self.cols - 1)
           y = random.randint(0, self.rows - 1)

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
