import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import spiral_simple_circle
import spiral_simple_square

'''
EXPERIMENTAL
Plots graph that compares square to circular magnetorquers
'''


def get_data(trace_width):
    '''
    Queries other functions to get graph data of spirals.

    Parameters:
        spacing (float): The decrease in radius per revolution

    Returns:
        max_l, lengths, areas_square, areas_circle
    '''
    if trace_width == 0:
        max_l = 1000
    else:
        max_l = 450/trace_width

    lengths = np.linspace(0, max_l, 50)
    areas_square = [
        spiral_simple_square.spiral(l, trace_width, OUTER_RADIUS)[0]
        for l in lengths
    ]
    areas_circle = [
        spiral_simple_circle.spiral(l, trace_width, OUTER_RADIUS)[0]
        for l in lengths
    ]
    return max_l, lengths, areas_square, areas_circle


if __name__ == "__main__":

    # Constants
    INIT_SPACING = 0.5  # Initial slider position
    OUTER_RADIUS = 10  # Outer radius simulated

    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()

    # Draw the initial lines
    _, lengths, areas_square, areas_circle = get_data(INIT_SPACING)
    line_square,  = ax.plot(lengths, areas_square, '-s', label='Square spiral')
    line_circle, = ax.plot(lengths, areas_circle, '-o',
                           label="Circular spiral")

    # Add all the labels
    ax.set_title("radius is set to 10 units")
    ax.set_xlabel('Length')
    ax.set_ylabel('Area-sum')
    ax.legend()

    # Adjust the main plot to make room for the sliders
    fig.subplots_adjust(bottom=0.25)

    # Make a horizontal slider to control the spacing.
    ax_spacing = fig.add_axes([0.25, 0.1, 0.6, 0.04])
    width_slider = Slider(
        ax=ax_spacing,
        label='Spacing',
        valmin=0,
        valmax=1,
        valinit=INIT_SPACING,
    )

    # The function to be called anytime a slider's value changes

    def update(_):

        # Collect updated data
        max_l, lengths, areas_square, areas_circle = get_data(width_slider.val)

        # Redraw the lines with the new data
        line_square.set_data(lengths, areas_square)
        line_circle.set_data(lengths, areas_circle)

        # Rescale the graph to fit the data
        max_y = max(areas_square)
        ax.set_xlim(-0.05*max_l, max_l)
        ax.set_ylim(-0.05*max_y, 1.05*max_y)

        fig.canvas.draw_idle()

    width_slider.on_changed(update)

    plt.show()
