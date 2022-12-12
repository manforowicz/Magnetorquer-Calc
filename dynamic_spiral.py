import math
from scipy import integrate
from scipy import optimize
from pathlib import Path
from configparser import ConfigParser
from unit_conversions import *

'''
Helper functions that calculate geometric properties of dynamic spirals
'''

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


def custom_spacing(multiplier, radius):

    # Returns radius (mm), ohms_per_mm
    width = multiplier / radius**1 #- config.getfloat("GapBetweenTraces")


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

    while r > inner_radius:

        outer_spacing = inner_spacing

        width, ohms_per_mm = trace_width_func(trace_width_multiplier, r)
        
        
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

    

    return area_sum * 1e-6, ohms


def spiral_of_resistance(ohms):

    def func(trace_width_multiplier):
        return spiral(trace_width_multiplier, custom_spacing)[1] - ohms

    trace_width_multiplier = optimize.brentq(func, 1e-9, 1e9)
    return spiral(trace_width_multiplier, custom_spacing)[0]


print("{:.4f}".format(spiral_of_resistance(100)))
