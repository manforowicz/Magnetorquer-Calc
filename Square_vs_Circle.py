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

print("Circle:")
print(properties_of_circle_spiral(35000, 1, 100))

print("\nSquare:")
print(properties_of_square_spiral(35000, 1, 100))




# Define initial parameters
init_spacing = 1

lengths = np.linspace(1, 2000, 100)
areas_square = [properties_of_square_spiral(length, init_spacing, 100) for length in lengths]
areas_circle = [properties_of_circle_spiral(length, init_spacing, 100) for length in lengths]

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line_square = ax.scatter(lengths, areas_square)
line_circle = ax.scatter(lengths, areas_circle)



ax.set_xlabel('Length')
ax.set_ylabel('Area-sum')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the spacing.
ax_spacing = fig.add_axes([0.25, 0.1, 0.65, 0.03])
spacing_slider = Slider(
    ax=ax_spacing,
    label='Spacing',
    valmin=0.1,
    valmax=30,
    valinit=init_spacing,
)


ax_length = fig.add_axes([0.25, 0.0, 0.65, 0.03])
length_slider = Slider(
    ax=ax_length,
    label='Length range',
    valmin=0.1,
    valmax=10000,
    valinit=1000,
)


# The function to be called anytime a slider's value changes
def update(_):
    s = spacing_slider.val
    max_l = length_slider.val
    lengths = np.linspace(1, max_l, 100)
    areas_square = [properties_of_square_spiral(length, s, 100) for length in lengths]
    areas_circle = [properties_of_circle_spiral(length, s, 100) for length in lengths]

    line_square.set_offsets(np.c_[lengths, areas_square])
    line_circle.set_offsets(np.c_[lengths, areas_circle])


    fig.canvas.draw_idle()


# register the update function with each slider
spacing_slider.on_changed(update)
length_slider.on_changed(update)


plt.show()