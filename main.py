import sys
from solve import *
from static_visual import draw_sudoku_static
from dynamic_visual import draw_sudoku_dynamic


def parse_input(filename):
    with open(filename) as file:
        sudoku_matrix = [list(map(int, line.strip().split())) for line in file if line.strip()]
    sudoku_matrix = np.array(sudoku_matrix)

    fixed_positions = set(
        (i, j) for i in range(sudoku_matrix.shape[0]) for j in range(sudoku_matrix.shape[1]) if sudoku_matrix[i, j] != 0
    )
    return sudoku_matrix, fixed_positions


def init_sudoku(grid, mutation_type):
    grid_size = grid.shape[0]
    random_board = grid.copy()
    if mutation_type == "row_swap":
        for row in range(grid_size):
            existing_numbers = set(grid[row, :]) - {0}
            valid_numbers = list(set(range(1, grid_size + 1)) - existing_numbers)
            np.random.shuffle(valid_numbers)
            for col in range(grid_size):
                if random_board[row, col] == 0:
                    random_board[row, col] = valid_numbers.pop()
    elif mutation_type == "block_swap":
        block_size = int(np.sqrt(grid_size))
        for row in range(0, grid_size, block_size):
            for col in range(0, grid_size, block_size):
                existing_numbers = set(grid[row:row + block_size, col:col + block_size].flatten()) - {0}
                valid_numbers = list(set(range(1, grid_size + 1)) - existing_numbers)
                np.random.shuffle(valid_numbers)
                for i in range(block_size):
                    for j in range(block_size):
                        if random_board[row + i, col + j] == 0:
                            random_board[row + i, col + j] = valid_numbers.pop()
    elif mutation_type == "random_swap":
        for row in range(grid_size):
            for col in range(grid_size):
                if random_board[row, col] == 0:
                    random_board[row, col] = np.random.randint(1, grid_size + 1)

    return random_board


def print_sudoku(sudoku_matrix, fixed_positions, algorithm, visual):
    initial_sudoku = init_sudoku(sudoku_matrix, mutation_type=algorithm)
    result, frames, algorithm_name = hill_climbing(calculate_fitness, initial_sudoku, fixed_positions, mutation_type=algorithm)
    print("Final Fitness (total error) is ", calculate_fitness(result))
    if visual == 'static':
        draw_sudoku_static(result, fixed_positions)
    elif visual == 'dynamic':
        draw_sudoku_dynamic(frames, fixed_positions, algorithm_name)


def main():
    filename = sys.argv[1]
    algorithm = sys.argv[2]
    algorithm_type = sys.argv[3] if algorithm == 'hillclimbing' else None
    visual = sys.argv[4] if algorithm == 'hillclimbing' else sys.argv[3]
    sudoku_matrix, fixed_positions = parse_input('sudoku/' + filename)
    print("Initial Sudoku Grid:")
    print(sudoku_matrix)
    print("-" * 40)
    if algorithm == 'backtracking':
        frames = solve_backtracking(sudoku_matrix, fixed_positions)
        if visual == 'static':
            draw_sudoku_static(sudoku_matrix, fixed_positions)
        elif visual == 'dynamic':
            draw_sudoku_dynamic(frames, fixed_positions, algorithm)
    elif algorithm == 'hillclimbing':
        print_sudoku(sudoku_matrix, fixed_positions, algorithm_type, visual)


if __name__ == '__main__':
    main()