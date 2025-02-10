import sys
from solve import *

def parse_input(filename):
    with open(filename) as file:
        sudoku_matrix = [list(map(int, line.strip().split())) for line in file if line.strip()]
    sudoku_matrix = np.array(sudoku_matrix)
    fixed_positions = set(
        (i, j) for i in range(sudoku_matrix.shape[0]) for j in range(sudoku_matrix.shape[1]) if sudoku_matrix[i, j] != 0
    )
    return sudoku_matrix, fixed_positions


def init_sudoku(grid):
    grid_size = grid.shape[0]
    random_board = grid.copy()
    for row in range(grid_size):
        existing_numbers = set(grid[row, :]) - {0}
        valid_numbers = list(set(range(1, grid_size + 1)) - existing_numbers)
        np.random.shuffle(valid_numbers)
        for col in range(grid_size):
            if random_board[row, col] == 0:
                random_board[row, col] = valid_numbers.pop()

    return random_board

def main():
    sudoku_matrix, fixed_positions = parse_input('sudoku.txt')
    algorithm = sys.argv[1]
    print("Initial Sudoku Grid:")
    print(sudoku_matrix)
    print("-" * 40)
    if algorithm == 'backtracking':
        solve_backtracking(sudoku_matrix, fixed_positions)
        print("Sudoku Grid:")
        print(sudoku_matrix)
        print("Fitness is ", calculate_fitness(sudoku_matrix))
        print("-" * 40)
    elif algorithm == 'hillclimbing':
        initial_sudoku = init_sudoku(sudoku_matrix)
        print("Initial Sudoku Grid:")
        print(initial_sudoku)
        result = hill_climbing(calculate_fitness, initial_sudoku, fixed_positions, max_iterations=1000)
        print("Sudoku Grid:")
        print(result)
        print("Fitness is ", calculate_fitness(result))
        print("-" * 40)
if __name__ == '__main__':
    main()