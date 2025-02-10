import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



def animate_sudoku(grids, interval=50):
    """
    Animates the solving process of Sudoku using Matplotlib.

    :param grids: List of 2D NumPy arrays representing each step of the solving process.
    :param interval: Time delay (in ms) between frames.
    """
    fig, ax = plt.subplots()
    ax.set_title("Sudoku Solving Progress")

    # Display the first frame
    grid_size = grids[0].shape[0]
    im = ax.imshow(grids[0], cmap="coolwarm", vmin=1, vmax=grid_size)

    def update(frame_idx):
        ax.set_title(f"Step {frame_idx + 1}")
        im.set_array(grids[frame_idx])
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(grids), interval=interval, repeat=False)
    plt.show()
