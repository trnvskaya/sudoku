import numpy as np
import random

def calculate_fitness(grid):
    rows = grid.shape[0]
    block_size = int(np.sqrt(rows))
    total_error = 0

    for i in range(rows):
        row_error = rows - len(set(grid[i, :]))
        col_error = rows - len(set(grid[:, i]))
        total_error += row_error + col_error

    for i in range(0, rows, block_size):
        for j in range(0, rows, block_size):
            block = grid[i:i + block_size, j:j + block_size]
            block_error = rows - len(set(block.flatten()))
            total_error += block_error

    return total_error


def is_valid (grid, row, col, num):
    if num in grid[row, :]:
        return False
    if num in grid[:, col]:
        return False
    block_size = int(np.sqrt(len(grid)))
    start_row, start_col = block_size * (row // block_size), block_size * (col // block_size)

    if num in grid [start_row:start_row+block_size, start_col:start_col+block_size]:
        return False
    return True


def solve_backtracking(grid, fixed_positions):
    rows, cols = grid.shape

    def backtrack():
        for row in range(rows):
            for col in range(cols):
                if (row, col) not in fixed_positions and grid[row, col] == 0:
                    for num in range(1, rows + 1):  # Try numbers 1 to N (N = rows)
                        if is_valid(grid, row, col, num):
                            grid[row, col] = num
                            if backtrack():
                                return True
                            grid[row, col] = 0  # Undo if no solution found

                    return False # No solution found
        return True

    return backtrack()

def hill_climbing(
        f: callable,
        x_init: np.array,
        fixed_positions: set,
        max_iterations=10000,
        restarts=10):

    grid_size = x_init.shape[0]
    best_grid = None
    best_error = float('inf')

    for _ in range(restarts):
        current_grid = x_init.copy()
        current_error = f(current_grid)

        for _ in range(max_iterations):
            mutable_positions = [(row, col) for row in range(grid_size) for col in range(grid_size)
                                 if (row, col) not in fixed_positions]

            if len(mutable_positions) < 2:
                break  # No moves possible

            # Pick two **random** mutable cells within the **same row**
            row = random.choice(range(grid_size))
            row_positions = [col for col in range(grid_size) if (row, col) in mutable_positions]

            if len(row_positions) < 2:
                continue  # Skip this iteration if not enough mutable numbers

            col1, col2 = random.sample(row_positions, 2)

            new_grid = current_grid.copy()
            new_grid[row, col1], new_grid[row, col2] = new_grid[row, col2], new_grid[row, col1]

            new_error = f(new_grid)

            if new_error < current_error:  # Accept better moves
                current_grid, current_error = new_grid, new_error

            if current_error == 0:
                return current_grid, 0

        if current_error < best_error:
            best_grid, best_error = current_grid, current_error

    return best_grid




