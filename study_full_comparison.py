from spiral_dynamic_square import *
import matplotlib.pyplot as plt
import numpy as np
import spiral_dynamic_square
import spiral_simple_circle
import spiral_simple_square


def get_data(func, label, *args):
    x = ohms_list
    y = [func(ohms, True, *args)[0] for ohms in x]

    ax.plot(x, y, '-o', label=label)
    return ohms_list,


# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

# Draw the initial lines
ohms_list = np.linspace(1, 1000, 100)
get_data(
    spiral_simple_circle.spiral_of_resistance, "Simple circle")
get_data(
    spiral_simple_square.spiral_of_resistance, "Simple square")
get_data(
    spiral_dynamic_square.spiral_of_resistance, "Dynamic Square")
get_data(
    spiral_dynamic_square.spiral_of_resistance, "Dynamic Square Simple Radius", spiral_dynamic_square.radius_proportional)
get_data(
    spiral_dynamic_square.spiral_of_resistance, "Dynamic Square Constant", spiral_dynamic_square.constant)

# Add all the labels
ax.set_xlabel('Ohms')
ax.set_ylabel('Area Sum (m^2)')
ax.legend()

plt.show()
