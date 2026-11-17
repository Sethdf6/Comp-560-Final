class Board:
    def __init__(self, size, grid = None):
        self.size = size
        self.grid = ([[0 for _ in range(size)] for _ in range(size)] if grid is None else [row.copy() for row in grid])

    def copy(self):
        return Board(self.size, self.grid)

    def get_empty_cells(self):
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j] == 0]

    def get_tile(self, row, col):
        return self.grid[row][col]

    def set_tile(self, row, col, value):
        self.grid[row][col] = value

    def get_max_tile(self):
        return max((max(row) for row in self.grid), default=0)

    def is_board_full(self):
        return all(cell != 0 for row in self.grid for cell in row)

    
    def __str__(self):
        cell_width = 6
        border = '+' + '+'.join(['-' * cell_width] * self.size) + '+'
        rows = [border]

        for row in self.grid:
            row_str = '|'.join(
                f'{cell:^{cell_width}}' if cell != 0 else ' ' * cell_width
                for cell in row
            )
            rows.append('|' + row_str + '|')
            rows.append(border)

        return '\n'.join(rows)


    