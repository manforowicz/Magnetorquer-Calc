from dynamic_spiral import *
import matplotlib.pyplot as plt
import numpy as np



def get_data(ohms_list, func):
    return [spiral_of_resistance(ohms, func)[0] for ohms in ohms_list]


# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

# Draw the initial lines
ohms_list = np.linspace(0.1, 10, 100)
line, = ax.plot(ohms_list, get_data(ohms_list, radius_proportional), '-o', label="trace_proporitional")

#line2, = ax.plot(ohms_list, get_data(ohms_list, total_spacing_proportional), '-o', label="total_spacing_proportional")

line3, = ax.plot(ohms_list, get_data(ohms_list, constant), '-o', label="constnt")

line4, = ax.plot(ohms_list, get_data(ohms_list, real_radius_proportional), '-o', label="advanced")

# Add all the labels
ax.set_xlabel('Ohms')
ax.set_ylabel('Area-sum')
ax.legend()

plt.show()