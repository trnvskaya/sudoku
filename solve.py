import numpy as np
import random
import random
import itertools
import copy


def init_sudoku(board, fixed_positions):
    random_board = board.copy()
    empty_positions = [
        (row, col) for row in range(9) for col in range(9) if (row, col) not in fixed_positions
    ]
    for row, col in empty_positions:
        random_board[row, col] = random.randint(1, 9)

    return random_board

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

def hill_climbing(grid, fixed_positions, max_iterations=10000, max_restarts = 10):
    best_solution = None
    best_fitness = float('inf')

    for i in range(max_restarts):
        current_sudoku = grid.copy()
        current_fitness = calculate_fitness(current_sudoku)

    pass

