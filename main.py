import numpy as np
import copy
import random

def parse_input(filename):
    """
    Parse input file to initialize the Sudoku board and fixed positions.
    """
    with open(filename) as file:
        sudoku_matrix = [list(map(int, line.strip().split())) for line in file if line.strip()]
    sudoku_matrix = np.array(sudoku_matrix)
    fixed_positions = set(
        (i, j) for i in range(sudoku_matrix.shape[0]) for j in range(sudoku_matrix.shape[1]) if sudoku_matrix[i, j] != 0
    )
    return sudoku_matrix, fixed_positions

def calculate_fitness(sudoku_matrix: np.array):
    row_error = sum(9 - len(set(row)) for row in sudoku_matrix)
    col_error = sum(9 -len(set(col)) for col in sudoku_matrix.T)
    block_error = 0
    for row_block in range(3):
        for col_block in range(3):
            block = sudoku_matrix[row_block * 3:(row_block+1) * 3][col_block * 3:(col_block+1) * 3]
            block_error += (9-len(set(block.flatten())))

    return row_error + col_error + block_error

def init_sudoku(board, fixed_positions):
    """
    Randomly fill non-fixed positions of the Sudoku board without validating constraints.
    """
    random_board = board.copy()
    empty_positions = [
        (row, col) for row in range(9) for col in range(9) if (row, col) not in fixed_positions
    ]
    for row, col in empty_positions:
        random_board[row, col] = random.randint(1, 9)

    return random_board

def generate_neighbors(sudoku_matrix, fixed_positions):
    neighbors = []
    pass

def hill_climbing(sudoku_matrix, fixed_positions):
    pass

def main():
    sudoku_matrix, fixed_positions = parse_input('sudoku.txt')
    print(sudoku_matrix)
    sudoku_matrix_init = init_sudoku(sudoku_matrix, fixed_positions)
    print(sudoku_matrix_init)
    print(calculate_fitness(sudoku_matrix_init))

if __name__ == '__main__':
    main()