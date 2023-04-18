from spiral_simple_square import *
import matplotlib.pyplot as plt
import numpy as np

'''
EXPERIMENTAL
Plots graph that shows how magnetic moment varies with resistance
given constant watts of heat generation
'''

def get_moment(watts, resistance):
    
    area_sum = spiral_of_resistance(resistance, True)[0]

    current = math.sqrt(watts / resistance)

    return area_sum * current



def get_data(ohms_list):
    return [get_moment(0.25, ohms) for ohms in ohms_list]


if __name__ == "__main__":

    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()

    # Draw the initial lines
    ohms_list = np.linspace(1, 40, 100)
    data = get_data(ohms_list)

    line, = ax.plot(ohms_list, data, '-o', label="trace_proporitional")

    ax.set_title("assumes 0.25 watt power for 1 magnetorquer layer")


    plt.xlim([0, 1.1*max(ohms_list)])
    plt.ylim([0, 1.1*max(data)])

    # Add all the labels
    ax.set_xlabel('Ohms')
    ax.set_ylabel('Magnetic Moment')
    ax.legend()

    plt.show()