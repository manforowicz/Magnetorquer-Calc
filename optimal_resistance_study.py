from dynamic_spiral import *
import matplotlib.pyplot as plt
import numpy as np


def get_moment(watts, resistance):
    
    area_sum = spiral_of_resistance(resistance, radius_proportional)[0]

    current = math.sqrt(watts / resistance)

    return area_sum * current



def get_data(ohms_list, func):
    return [get_moment(0.5, ohms) for ohms in ohms_list]


# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

# Draw the initial lines
ohms_list = np.linspace(1, 100, 100)
line, = ax.plot(ohms_list, get_data(ohms_list, radius_proportional), '-o', label="trace_proporitional")

# Add all the labels
ax.set_xlabel('Ohms')
ax.set_ylabel('Magnetic Moment')
ax.legend()

plt.show()