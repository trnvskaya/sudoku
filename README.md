# Sudoku Solver with Visualization

This project provides a solver for Sudoku puzzles using two algorithms: **Backtracking** and **Hill Climbing**. It includes visualizations of the solving process, both static and dynamic, using Matplotlib. 

## Algorithm Workflow:

- **Hill Climbing** is used to solve the Sudoku puzzle iteratively. If no solution is found within the specified iterations or restarts, it automatically switches to Backtracking.
- **Backtracking** is used as a fallback to systematically explore all possible solutions until a valid one is found.


## Features:
- Solve Sudoku using **Backtracking** or **Hill Climbing** algorithms.
- Visualize the solving process with two options:
  - **Static Visualization**: A static representation of the final solution.
  - **Dynamic Visualization**: An animated view showing the steps taken during the solving process.
- Support for customizable mutation strategies in the Hill Climbing algorithm: **row_swap**, **block_swap**, and **random_swap**.

## Requirements:
- Python 3.x
- Required libraries: 
  - `numpy`
  - `matplotlib`
  - `random`

Install required libraries with:
```bash
pip install numpy matplotlib
```

## Usage:

To run the solver, use the following command:
```bash
python main.py <filename> <algorithm> [<hillclimbing_mutation_type>] <visualization>
```
### Parameters:

- **filename**: The filename of the Sudoku puzzle (in text format) to be solved. The file should contain a 9x9 grid with numbers separated by spaces. Zeros represent empty cells.
- **algorithm**: The algorithm to use for solving:
  - `backtracking`: Use the backtracking algorithm to solve the puzzle.
  - `hillclimbing`: Use the Hill Climbing algorithm.
- **visualization**: Type of visualization:
  - `static`: Display a static image of the final solution.
  - `dynamic`: Show an animated process of the solving steps.
- **hillclimbing_mutation_type** (only if using hillclimbing): The mutation strategy used for Hill Climbing:
  - `row_swap`: Swap two rows.
  - `block_swap`: Swap two blocks.
  - `random_swap`: Randomly swap two cells.
 
### Example Usage:

Backtracking with Static Visualization:

```bash
python main.py puzzle.txt backtracking static
```

Hill Climbing with Dynamic Visualization (using row_swap mutation):

```bash
python main.py puzzle.txt hillclimbing dynamic row_swap
```


## File Format for Puzzle Input:

The input file should be a text file containing the Sudoku grid. Zeros represent empty cells.

`Example of sudoku.txt:`

```bash
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
```
