from spiral_dynamic_square import *
import matplotlib.pyplot as plt
import numpy as np
import spiral_dynamic_square, spiral_simple_circle, spiral_simple_square


def get_data(func, label, *args):
    x = ohms_list
    y = [func(ohms, True, *args)[0] for ohms in x]
    
    ax.plot(x, y, '-o', label=label)
    return ohms_list, 


# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

# Draw the initial lines
ohms_list = np.linspace(1, 100, 100)
simple_circle_line = get_data(spiral_simple_circle.spiral_of_resistance, "Simple circle")
simple_square_line = get_data(spiral_simple_square.spiral_of_resistance, "Simple square")
dynamic_square_line = get_data(spiral_dynamic_square.spiral_of_resistance, "Dynamic Square", spiral_dynamic_square.constant)

# Add all the labels
ax.set_xlabel('Ohms')
ax.set_ylabel('Area Sum (m^2)')
ax.legend()

plt.show()