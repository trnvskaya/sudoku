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
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in fixed_positions:
                grid[row, col] = 0

    frames = []

    def backtrack():
        for row in range(rows):
            for col in range(cols):
                if (row, col) not in fixed_positions and grid[row, col] == 0:
                    for num in range(1, rows + 1):  # Try numbers 1 to N (N = rows)
                        if is_valid(grid, row, col, num):
                            grid[row, col] = num
                            frames.append(grid.copy())
                            if backtrack():
                                return True
                            grid[row, col] = 0  # Undo if no solution found
                            frames.append(grid.copy())

                    return False # No solution found
        return True

    backtrack()
    return frames


def hill_climbing(
        f: callable,
        x_init: np.array,
        fixed_positions: set,
        max_iterations=5000,
        restarts=10,
        mutation_type="row_swap"):

    grid_size = x_init.shape[0]
    best_grid = None
    best_error = float('inf')
    algorithm_name = "Hill Climbing"

    frames = []

    for _ in range(restarts):
        current_grid = x_init.copy()
        frames.append(current_grid.copy())
        current_error = f(current_grid)

        for _ in range(max_iterations):
            mutable_positions = [(row, col) for row in range(grid_size) for col in range(grid_size)
                                 if (row, col) not in fixed_positions]

            if len(mutable_positions) < 2:
                break  # No moves possible

            row1, col1, row2, col2 = None, None, None, None

            if mutation_type == "row_swap":
                row1 = random.choice(range(grid_size))
                row_positions = [col for col in range(grid_size) if (row1, col) in mutable_positions]

                if len(row_positions) < 2:
                    continue

                col1, col2 = random.sample(row_positions, 2)
                row2 = row1 # Have to be in the same row

            elif mutation_type == "block_swap":
                block_size = int(np.sqrt(grid_size))
                block_row = random.choice(range(0, grid_size, block_size))
                block_col = random.choice(range(0, grid_size, block_size))

                block_positions = [(r, c) for r in range(block_row, block_row + block_size)
                                   for c in range(block_col, block_col + block_size)
                                   if (r, c) in mutable_positions]

                if len(block_positions) < 2:
                    continue

                (row1, col1), (row2, col2) = random.sample(block_positions, 2)

            elif mutation_type == "random_swap":
                (row1, col1), (row2, col2) = random.sample(mutable_positions, 2)

            new_grid = current_grid.copy()
            new_grid[row1, col1], new_grid[row2, col2] = new_grid[row2, col2], new_grid[row1, col1]
            frames.append(new_grid.copy())

            new_error = f(new_grid)

            if new_error < current_error:
                current_grid, current_error = new_grid, new_error

            if current_error == 0:
                return current_grid, frames, algorithm_name

        if current_error < best_error:
            best_grid, best_error = current_grid, current_error
    if calculate_fitness(best_grid) != 0:
        frames_new = solve_backtracking(
            best_grid,
            fixed_positions)
        frames.extend(frames_new)
        algorithm_name = "Hill Climbing with Backtracking"
    return best_grid, frames, algorithm_name