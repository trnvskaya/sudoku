import numpy as np
import random
from tqdm import tqdm
import itertools
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

if __name__ == '__main__':
    main()