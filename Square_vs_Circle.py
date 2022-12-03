import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy import integrate
from scipy import optimize


# Returns length of spiral. Proof: https://planetcalc.com/3707/
def length_of_circle_spiral(a, b, theta):
    return integrate.quad(lambda t: math.sqrt((a - b*t)**2 + b**2), 0, theta)[0]


# Returns sum of coil areas
def area_sum_of_circle_spiral(a, b, theta):
    return integrate.quad(lambda t: 0.5*(a - b*t)**2, 0, theta)[0]

def properties_of_circle_spiral(length, spacing, outer_radius):

    a = outer_radius
    b = spacing / (2 * math.pi)

    if b == 0:  # If b is 0 we have a perfect circle
        theta = length / a  # Circle arc length formula
    else:
        # a/b gives theta that results in 0 inner radius
        # If user gives a greater length, use that (even though it physically won't fit)
        max_theta = max(length/b, a/b)

        # Use math to find theta that gives a spiral of the desired length
        theta = optimize.brentq(
            lambda t: length_of_circle_spiral(a, b, t) - length, 0, max_theta)

    # Calculate and return other properties from theta
    inner_radius = a - b*theta
    if inner_radius < 0: return float('nan')
    area_sum = area_sum_of_circle_spiral(a, b, theta)

    return  area_sum


def properties_of_square_spiral(length, spacing, outer_radius):
    r = outer_radius
    s = spacing
    
    length -= r*2
    area_sum = r**2

    if length > 0:
        while length > 0:
            length -= 4*r
            area_sum += 2 * r**2

            r -= s/2
            if r < 0: return float('nan')

        r += s/2
    if length < -2*r:
        area_sum -= r ** 2
        length += 2*r
    
    area_sum -= -length * r / 2
    
    return area_sum


# Define initial parameters
init_spacing = 0.5
init_length = 800
outer_radius = 10

lengths = np.linspace(0, init_length, 50)
areas_square = [properties_of_square_spiral(length, init_spacing, outer_radius) for length in lengths]
areas_circle = [properties_of_circle_spiral(length, init_spacing, outer_radius) for length in lengths]

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
ax.set_title("Note: radius is set to 10 units")
line_square = ax.scatter(lengths, areas_square, label='Square spiral')
line_circle = ax.scatter(lengths, areas_circle, label="Circular spiral")
ax.legend()



ax.set_xlabel('Length')
ax.set_ylabel('Area-sum')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the spacing.
ax_spacing = fig.add_axes([0.25, 0.1, 0.6, 0.04])
spacing_slider = Slider(
    ax=ax_spacing,
    label='Spacing',
    valmin=0,
    valmax=1,
    valinit=init_spacing,
)


ax_length = fig.add_axes([0.25, 0.05, 0.6, 0.04])
length_slider = Slider(
    ax=ax_length,
    label='Max length (zoom)',
    valmin=1,
    valmax=10000,
    valinit=init_length,
)


# The function to be called anytime a slider's value changes
def update(_):
    s = spacing_slider.val
    max_l = length_slider.val
    lengths = np.linspace(0, max_l, 50)
    areas_square = [properties_of_square_spiral(length, s, outer_radius) for length in lengths]
    areas_circle = [properties_of_circle_spiral(length, s, outer_radius) for length in lengths]

    line_square.set_offsets(np.c_[lengths, areas_square])
    line_circle.set_offsets(np.c_[lengths, areas_circle])

    max_y = max(areas_square)

    ax.set_xlim(-0.05*max_l, 1.05*max_l)
    ax.set_ylim(-0.05*max_y, 1.05*max_y)

    fig.canvas.draw_idle()


# register the update function with each slider
spacing_slider.on_changed(update)
length_slider.on_changed(update)


plt.show()