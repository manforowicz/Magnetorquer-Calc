import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy import integrate
from scipy import optimize


def length_of_circle_spiral(a: float, b: float, theta: float) -> float:
    '''
    Returns the length of a circular archimedean spiral.
    Proof: https://planetcalc.com/3707/

    Parameters:
        a (float): The outer radius of the spiral
        b (float): The decrease in radius per 1 radian of rotation
        theta (float): The number of radians
    
    Returns:
        Length (float): The length of the spiral
    '''
    return integrate.quad(lambda t: math.sqrt((a - b*t)**2 + b**2), 0, theta)[0]


def area_sum_of_circle_spiral(a: float, b: float, theta: float) -> float:
    '''
    Returns the sum of coil areas of a circular archimedean spiral.
    All else constant, area-sum is proportional to magnetorquer torque.

    Parameters:
        a (float): The outer radius of the spiral
        b (float): The decrease in radius per 1 radian of rotation
        theta (float): The number of radians
    
    Returns:
        Area-sum (float): The area-sum of the spiral
    '''
    return integrate.quad(lambda t: 0.5*(a - b*t)**2, 0, theta)[0]


def properties_of_circle_spiral(length: float, spacing: float, outer_radius: float) -> float:
    '''
    Returns the sum of coil areas of a circular archimedean spiral.
    All else constant, area-sum is proportional to magnetorquer torque.

    Parameters:
        length (float): The length of the spiral's line
        spacing (float): The decrease in radius per 1 turn of rotation
        outer_radius (float): The outer radius of the spiral
    
    Returns:
        Area-sum (float): The area-sum of the spiral
    '''
    a = outer_radius
    b = spacing / (2 * math.pi)

    if b == 0:  # If b is 0 we have a perfect circle
        theta = length / a  # Circle arc length formula
    else:
        # a/b gives theta that results in 0 inner radius  
        max_theta = a / b

        # If user gives a longer length, that won't fit, so return NaN
        if length > length_of_circle_spiral(a, b, max_theta):
            return float('nan')

        # Use math to find theta that gives a spiral of the desired length
        theta = optimize.brentq(
            lambda t: length_of_circle_spiral(a, b, t) - length, 0, max_theta)
    
    area_sum = area_sum_of_circle_spiral(a, b, theta)

    return area_sum


def properties_of_square_spiral(length, spacing, outer_radius):
    '''
    Returns the sum of coil areas of a square archimedean spiral.
    All else constant, area-sum is proportional to magnetorquer torque.

    Parameters:
        length (float): The length of the spiral's line
        spacing (float): The decrease in radius per 1 turn of rotation
        outer_radius (float): The outer radius of the spiral
    
    Returns:
        Area-sum (float): The area-sum of the spiral
    '''
    r = outer_radius
    s = spacing

    # Draw outer edge
    length -= r*2
    area_sum = r**2

    # Draw spiral, going to edges at a time.
    if length > 0:
        r += s/2
    while length > 0:
        r -= s/2
        if r < 0:
            return float('nan')

        length -= 4*r
        area_sum += 2 * r**2

    # If overshot by more than one edge, remove that edge
    if length < -2*r:
        area_sum -= r ** 2
        length += 2*r

    # Remove triangle area of overshot length
    area_sum -= -length * r / 2 

    return area_sum


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
        properties_of_square_spiral(l, spacing, OUTER_RADIUS)
        for l in lengths
    ]
    areas_circle = [
        properties_of_circle_spiral(l, spacing, OUTER_RADIUS)
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
fig.subplots_adjust(left=0.25, bottom=0.25)

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
