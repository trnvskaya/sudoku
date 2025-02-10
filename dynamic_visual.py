import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from static_visual import is_conflict

def draw_sudoku_dynamic(frames, fixed_positions):
    fig, ax = plt.subplots(figsize=(6, 6))

    def update(frame):
        ax.clear()
        grid = frames[frame]

        # Draw grid
        ax.set_xticks(np.arange(0, grid.shape[0] + 1, 1))
        ax.set_yticks(np.arange(0, grid.shape[1] + 1, 1))
        ax.grid(which="both", color="black", linewidth=1.5)
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                num = grid[i, j]
                color = "white"

                if (i, j) in fixed_positions:
                    color = "lightgreen"  # Fixed positions (green)
                elif num == 0:
                    color = "white"  # Empty cell
                elif is_conflict(grid, i, j):
                    color = "red"  # Conflict

                ax.add_patch(plt.Rectangle((j, grid.shape[0] - i - 1), 1, 1, color=color))

                if num > 0:
                    ax.text(j + 0.5, grid.shape[0] - i - 0.5, str(num), ha="center", va="center", fontsize=14)

    ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=50, repeat=False)
    plt.show()