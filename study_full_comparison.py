from spiral_dynamic_square import *
import matplotlib.pyplot as plt
import numpy as np
import spiral_dynamic_square, spiral_simple_circle, spiral_simple_square



def get_data(func):
    return ohms_list, [func(ohms, True)[0] for ohms in ohms_list]


# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

# Draw the initial lines
ohms_list = np.linspace(1, 100, 100)
simple_circle_line = ax.plot(*get_data(spiral_simple_circle.spiral_of_resistance), '-o', label="Simple Circle")
simple_square_line = ax.plot(*get_data(spiral_simple_square.spiral_of_resistance), '-o', label="Simple Square")
dynamic_square_line = ax.plot(*get_data(spiral_dynamic_square.spiral_of_resistance), '-o', label="Dynamic Square")

# Add all the labels
ax.set_xlabel('Ohms')
ax.set_ylabel('Area Sum')
ax.legend()

plt.show()