import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from spirals import properties_of_square_spiral, properties_of_round_spiral
#### PLOTTING THE GRAPH ####


def get_data(spacing):
    '''
    Queries other functions to get graph data of spirals.

    Parameters:
        spacing (float): The decrease in radius per revolution
    
    Returns:
        max_l, lengths, areas_square, areas_circle
    '''
    if spacing == 0:
        max_l = 50000
    else:
        max_l = 450/spacing

    lengths = np.linspace(0, max_l, 50)
    areas_square = [
        properties_of_square_spiral(l, spacing, OUTER_RADIUS)[2]
        for l in lengths
    ]
    areas_circle = [
        properties_of_round_spiral(l, spacing, OUTER_RADIUS)[2]
        for l in lengths
    ]
    return max_l, lengths, areas_square, areas_circle


# Constants
INIT_SPACING = 0.5 # Initial slider position
OUTER_RADIUS = 10 # Outer radius simulated


# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

# Draw the initial lines
_, lengths, areas_square, areas_circle = get_data(INIT_SPACING)
line_square,  = ax.plot(lengths, areas_square, '-s', label='Square spiral')
line_circle, = ax.plot(lengths, areas_circle, '-o', label="Circular spiral")

# Add all the labels
ax.set_title("radius is set to 10 units")
ax.set_xlabel('Length')
ax.set_ylabel('Area-sum')
ax.legend()


# Adjust the main plot to make room for the sliders
fig.subplots_adjust(bottom=0.25)

# Make a horizontal slider to control the spacing.
ax_spacing = fig.add_axes([0.25, 0.1, 0.6, 0.04])
spacing_slider = Slider(
    ax=ax_spacing,
    label='Spacing',
    valmin=0,
    valmax=1,
    valinit=INIT_SPACING,
)


# The function to be called anytime a slider's value changes
def update(_):

    # Collect updated data
    max_l, lengths, areas_square, areas_circle = get_data(spacing_slider.val)

    #Redraw the lines with the new data
    line_square.set_data(lengths, areas_square)
    line_circle.set_data(lengths, areas_circle)

    # Rescale the graph to fit the data
    max_y = max(areas_square)
    ax.set_xlim(-0.05*max_l, max_l)
    ax.set_ylim(-0.05*max_y, 1.05*max_y)

    fig.canvas.draw_idle()


spacing_slider.on_changed(update)

plt.show()
