import math
from scipy import optimize
from pathlib import Path
from configparser import ConfigParser
from unit_conversions import *
import matplotlib.pyplot as plt
import numpy as np

'''
Helper functions that calculate geometric properties of dynamic spirals
'''

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


def trace_proportional(multiplier, radius, _):

    # Returns radius (mm), ohms_per_mm
    width = multiplier / radius**1
    return width, get_ohms_per_mm(width, True)


def total_spacing_proportional(multiplier, radius, _):

    # Returns radius (mm), ohms_per_mm
    width = multiplier / radius**1 - config.getfloat("GapBetweenTraces")
    return width, get_ohms_per_mm(width, True)

def constant(multiplier, radius, _):
    return multiplier, get_ohms_per_mm(multiplier, True)

def custom(multiplier, radius, outer_spacing):
    gap = config.getfloat("GapBetweenTraces")
    
    def func(width):

        resistance = 1e4 * multiplier * (8*radius + outer_spacing -gap-width) / width
        area_value = radius**3 - (radius-gap-width)**3
        #print(resistance-area_value)
        return resistance - area_value
    
    width = optimize.brentq(func, 1e-6, 1e6)

    return width, get_ohms_per_mm(width, True)



def spiral(trace_width_multiplier, trace_width_func, inner_radius=None, outer_radius=None):

    # Note: Starts on the outside, and spirals inwards

    gap = config.getfloat("GapBetweenTraces")

    if inner_radius == None:
        inner_radius = 5
    
    if outer_radius == None:
        outer_radius = config.getfloat("OuterRadius")

    r = outer_radius
    area_sum = 0
    ohms = 0
    inner_spacing = 0
    coils = 0

    while r > inner_radius:

        outer_spacing = inner_spacing

        width, ohms_per_mm = trace_width_func(trace_width_multiplier, r, outer_spacing)
        
        
        if math.isnan(ohms_per_mm): 
            return float("nan"), float("inf")

        inner_spacing = width + gap

        area_sum += 4 * r**2
        area_sum += 0.5*r * outer_spacing
        area_sum -= 0.5*r * inner_spacing

        ohms += ohms_per_mm * 8 * r
        ohms += ohms_per_mm * outer_spacing
        ohms -= ohms_per_mm * inner_spacing

        r -= inner_spacing
        coils += 1

    area_sum_m = area_sum * 1e-6

    return area_sum_m, ohms, coils


def spiral_of_resistance(ohms, trace_width_func):

    def func(trace_width_multiplier):
        return spiral(trace_width_multiplier, trace_width_func)[1] - ohms

    trace_width_multiplier = optimize.brentq(func, 1e-9, 1e9)
    return spiral(trace_width_multiplier, trace_width_func)


print("Area sum (m^2): {:.4f} {:.4f} {:.4f}".format(*spiral_of_resistance(1, trace_proportional)))


### GRAPH ###

def get_data(ohms_list, func):
    return [spiral_of_resistance(ohms, func)[0] for ohms in ohms_list]


# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

# Draw the initial lines
ohms_list = np.linspace(0.1, 10, 100)
line, = ax.plot(ohms_list, get_data(ohms_list, trace_proportional), '-o', label="trace_proporitional")

line2, = ax.plot(ohms_list, get_data(ohms_list, total_spacing_proportional), '-o', label="total_spacing_proportional")

line3, = ax.plot(ohms_list, get_data(ohms_list, constant), '-o', label="constnt")

line4, = ax.plot(ohms_list, get_data(ohms_list, custom), '-o', label="advanced")

# Add all the labels
ax.set_xlabel('Ohms')
ax.set_ylabel('Area-sum')
ax.legend()

plt.show()