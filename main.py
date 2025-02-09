import numpy as np
import random
from tqdm import tqdm
import itertools

def parse_input(filename):
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
            block = sudoku_matrix[row_block * 3:(row_block+1) * 3, col_block * 3:(col_block+1) * 3]
            block_error += (9-len(set(block.flatten())))

    return row_error + col_error + block_error

def is_valid(board, row, num):
    if num in board[row, :]:
        return False
    return True

def init_sudoku(board, fixed_positions):
    random_board = board.copy()
    for row in range(9):
        for col in range(9):
            if (row, col) not in fixed_positions:
                valid_numbers = [num for num in range(1, 10) if is_valid(random_board, row, num)]
                if valid_numbers:
                    random_board[row, col] = random.choice(valid_numbers)
    return random_board

def random_neighbor(x, fixed_positions):
    mutable_positions = [
        (row, col)
        for row in range(9) for col in range(9)
        if (row, col) not in fixed_positions
    ]
    if len(mutable_positions) < 2:
        return x

    pos1, pos2 = random.sample(mutable_positions, 2)
    neighbor = x.copy()
    neighbor[pos1[0], pos1[1]], neighbor[pos2[0], pos2[1]] = (
        neighbor[pos2[0], pos2[1]],
        neighbor[pos1[0], pos1[1]],
    )
    return neighbor


def best_neighbor(x, fixed_positions, fitness_func):
    mutable_positions = [
        (row, col)
        for row in range(9) for col in range(9)
        if (row, col) not in fixed_positions
    ]

    if len(mutable_positions) < 2:
        return x

    best_fitness = float('inf')
    best_neighbor = x.copy()

    for pos1, pos2 in itertools.combinations(mutable_positions, 2):
        neighbor = x.copy()
        neighbor[pos1[0], pos1[1]], neighbor[pos2[0], pos2[1]] = (
            neighbor[pos2[0], pos2[1]],
            neighbor[pos1[0], pos1[1]],
        )

        neighbor_fitness = fitness_func(neighbor)
        if neighbor_fitness < best_fitness:
            best_fitness = neighbor_fitness
            best_neighbor = neighbor

    return best_neighbor


def hill_climbing(f: callable, x_init: np.array, n_iters: int, fixed_positions, variant: str, steepest: bool = False):
    x = x_init.copy()
    x_best = x_init.copy()

    neighbor_function = random_neighbor if variant == 'simple' else (lambda x, fp: best_neighbor(x, fp, f))

    for iteration in tqdm(range(n_iters)):
        y = neighbor_function(x, fixed_positions)
        if f(y) < f(x):
            x = y
            if f(x) < f(x_best):
                x_best = x
        elif steepest:
            x = x_best

    return x_best

def main():
    sudoku_matrix, fixed_positions = parse_input('sudoku.txt')
    print("Initial Sudoku Grid:")
    print(sudoku_matrix)
    print("-" * 40)

    sudoku_matrix_init = init_sudoku(sudoku_matrix, fixed_positions)
    print("Initialized Sudoku Grid:")
    print(sudoku_matrix_init)
    print("Initialized Fitness:", calculate_fitness(sudoku_matrix_init))
    print("-" * 40)

    # Call hill climbing
    sudoku_matrix_final = hill_climbing(
        f=calculate_fitness,
        x_init=sudoku_matrix_init,
        n_iters=50000,
        fixed_positions=fixed_positions,
        variant="simple",
        steepest=True,
    )

    print("Final Sudoku Grid:")
    print(sudoku_matrix_final)
    print("Final Fitness:", calculate_fitness(sudoku_matrix_final))

if __name__ == '__main__':
    main()