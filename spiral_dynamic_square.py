import math
from scipy import optimize
from pathlib import Path
from configparser import ConfigParser
from helper_conversions import *
from output_KiCad_dynamic_spiral import SpiralShape

'''
EXPERIMENTAL
Functions that define a variable trace width square spiral
'''

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


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

# Actual program


def spiral(trace_width_multiplier, trace_width_func, exterior, return_shape=False):

    # Note: Starts on the outside, and spirals inwards

    inner_radius = 5
    outer_radius = config.getfloat("OuterRadius")
    gap = config.getfloat("GapBetweenTraces")

    if return_shape:
        shape = SpiralShape()

    area_sum = 0
    ohms = 0
    coils = 0

    current_r = outer_radius
    prev_r = outer_radius

    current_width = trace_width_func(trace_width_multiplier, current_r)

    while current_r + 0.5 * current_width > inner_radius:

        next_r = current_r - 0.5 * current_width - gap
        next_width = trace_width_func(trace_width_multiplier, next_r)
        next_r -= 0.5 * next_width

        length = 6*current_r + prev_r + next_r
        area_sum += 0.5 * length * current_r
        ohms += get_ohms_per_mm(current_width, exterior) * length
        coils += 1

        # Drawing
        if return_shape:
            a = (outer_radius - prev_r, outer_radius - current_r)
            b = (outer_radius + current_r, outer_radius - current_r)
            c = (outer_radius + current_r, outer_radius + current_r)
            d = (outer_radius - current_r, outer_radius + current_r)
            e = (outer_radius - current_r, outer_radius - next_r)
            shape.add_coil(current_width, a, b, c, d, e)

        prev_r = current_r
        current_r = next_r
        current_width = next_width

    area_sum_m = area_sum * 1e-6

    if return_shape:
        return shape
    else:
        return area_sum_m, ohms, coils


def spiral_of_resistance(ohms, exterior, trace_width_func=real_radius_proportional, return_shape=False):

    def func(trace_width_multiplier):
        return spiral(trace_width_multiplier, trace_width_func, exterior)[1] - ohms

    trace_width_multiplier = optimize.brentq(func, 1e-6, 1e6)
    return spiral(trace_width_multiplier, trace_width_func, exterior, return_shape=return_shape)
