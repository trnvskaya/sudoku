import numpy as np
import matplotlib.pyplot as plt


def is_conflict(grid, row, col):

    num = grid[row, col]
    grid_size = grid.shape[0]
    block_size = int(np.sqrt(grid_size))

    if list(grid[row, :]).count(num) > 1 or list(grid[:, col]).count(num) > 1:
        return True

    start_row, start_col = (row // block_size) * block_size, (col // block_size) * block_size
    block = grid[start_row:start_row + block_size, start_col:start_col + block_size]
    if list(block.flatten()).count(num) > 1:
        return True
    return False


def draw_sudoku_static(grid, fixed_positions):
    grid_size = grid.shape[0]
    block_size = int(np.sqrt(grid_size))

    fig, ax = plt.subplots(figsize=(6, 6))

    for i in range(grid_size + 1):
        lw = 2 if i % block_size == 0 else 0.5
        ax.plot([i, i], [0, grid_size], "k", lw=lw)
        ax.plot([0, grid_size], [i, i], "k", lw=lw)

    for row in range(grid_size):
        for col in range(grid_size):
            num = grid[row, col]
            if num == 0:
                continue

            if (row, col) in fixed_positions:
                color = "green"
            elif is_conflict(grid, row, col):
                color = "red"
            else:
                color = "white"

            ax.add_patch(plt.Rectangle((col, grid_size - row - 1), 1, 1, color=color))

            ax.text(col + 0.5, grid_size - row - 0.5, str(num),
                    ha="center", va="center", fontsize=14, color="black")

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_title("Sudoku Visualization")
    plt.show()