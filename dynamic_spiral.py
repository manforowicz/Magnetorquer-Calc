import math
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


def spiral(trace_width_multiplier, trace_width_func, exterior):

    # Note: Starts on the outside, and spirals inwards

    inner_radius = config.getfloat("InnerRadius")
    outer_radius = config.getfloat("OuterRadius")
    gap = config.getfloat("GapBetweenTraces")

    area_sum = 0
    ohms = 0
    coils = 0

    current_r = outer_radius
    prev_r = outer_radius

    current_width = trace_width_func(trace_width_multiplier, current_r)
    current_r -= 0.5 * current_width

    while current_r + 0.5 * current_width > inner_radius:

        next_r = current_r - 0.5 * current_width - gap
        next_width = trace_width_func(trace_width_multiplier, next_r)
        next_r -= 0.5 * next_width

        length = 8*current_r + (prev_r - current_r) - (current_r - next_r)
        area_sum += 0.5 * length * current_r
        ohms += get_ohms_per_mm(current_width, exterior) * length
        coils += 1

        prev_r = current_r
        current_r = next_r
        current_width = next_width

    area_sum_m = area_sum * 1e-6

    return area_sum_m, ohms, coils


def spiral_of_resistance(ohms, trace_width_func, exterior):

    def func(trace_width_multiplier):
        return spiral(trace_width_multiplier, trace_width_func, exterior)[1] - ohms

    trace_width_multiplier = optimize.brentq(func, 1e-6, 1e6)
    return spiral(trace_width_multiplier, trace_width_func, exterior)


# Different functions that relate radius to spacing

def radius_proportional(multiplier, radius):

    # Returns radius (mm), ohms_per_mm
    width = multiplier / radius**1
    return width


def spacing_proportional_to_radius(multiplier, radius):

    # Returns radius (mm), ohms_per_mm
    width = multiplier / radius**1 - config.getfloat("GapBetweenTraces")
    return width


def constant(multiplier, radius):
    return multiplier


def real_radius_proportional(multiplier, radius):

    if radius**2 <= 2 * multiplier:
        width = radius
    else:
        width = radius - math.sqrt(radius**2 - 2*multiplier)

    return width
