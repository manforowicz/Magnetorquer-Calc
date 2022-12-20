import math
import numpy as np
from scipy import optimize
from pathlib import Path
from configparser import ConfigParser
from spiral_simple_square import spiral
import output_KiCad_spiral
from unit_conversions import *

'''
Goal is to find coil that maximizes area-sum under the given constraints
Area-sum is the sum of the areas created by each coil
Assuming everything else is constant, area-sum is proportional to magnetorquer's torque

Spiral used is a square spiral similar to an archimedean spiral
This spiral is used due to its favorable characteristics demonstrated in square_vs_circle.py
'''


# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


# Returns max trace length physically possible.
# Takes outer radius and a function that defines spacing
def max_trace_length(resistance, outer_layer):
    '''
    Calculates the maximum length of wire that can fit on the spiral.

    Uses binary search and finds highest length that doesn't receive NaN
    from spirals.properties_of_square_spiral().

    Paramters:
        resistance (float - ohms): The intended resistance of the spiral.
        outer_layer (bool): States whether spiral is on outer layer of the PCB
                            since that influences trace thickness

    Returns:
        max_length (float - mm): Maximum length of wire that can fit on the spiral.

    '''
    lower = 0
    upper = 1e6 # TODO: Algorithmatize this hard coded value

    while upper - lower > upper*0.001:

        length_guess = (upper + lower)/2
        s = spacing_from_length(length_guess, resistance, outer_layer)

        if math.isnan(spiral(length_guess, s)[0]):
            upper = length_guess
        else:
            lower = length_guess

    max_length = lower

    return max_length


# Finds trace length tha maximizes area-sum
def spiral_of_resistance(resistance, outer_layer):
    '''
    Calculates the optimal properties of square spiral.
    Optimal properties means area-sum maximizing.

    Paramters:
        resistance (float - ohms): The intended resistance of the spiral.
        outer_layer (bool): States whether spiral is on outer layer of the PCB
                            since that influences trace thickness

    Returns:
        num_of_coils (float): Number of coils
        inner_radius (float - mm): Inner radius of spiral
        area_sum (float - mm^2): Area-sum of spiral
        spacing (float - mm): Spacing between coils
        length (float - mm): Length of PCB trace

    '''
    # Dummy function to meet requirements of `optimize.minimize_scalar`
    def neg_area_sum_from_length(length):
        s = spacing_from_length(length, resistance, outer_layer)
        return -spiral(length, s)[2]

    max_length = max_trace_length(resistance, outer_layer)
    # Finds length that gives maximum area-sum
    length = optimize.minimize_scalar(
        neg_area_sum_from_length,
        bounds=(0, max_length),
        method='bounded'
    ).x

    # Calculate data from the optimal length
    spacing = spacing_from_length(length, resistance, outer_layer)
    optimal = spiral(length, spacing)

    # Return coil spacing, number of coils, and area-sum
    return optimal[0], optimal[1], optimal[2], spacing, length



def find_total_area_sum_from_front_resistance(front_resistance):
    inner_resistance = inner_resistance_from_front_resistance(front_resistance)
    inner_layers = config.getint("NumberOfLayers") - 2

    area_sum = 0
    area_sum += 2 * spiral_of_resistance(front_resistance, True)[2]
    area_sum += inner_layers * spiral_of_resistance(inner_resistance, False)[2]
    return area_sum


def optimal_magnetorquer_front_resistance():
    front_resistance = optimize.minimize_scalar(
        lambda r: -find_total_area_sum_from_front_resistance(r),
        bounds=(0, config.getfloat("Resistance")/2),
        method='bounded'
    ).x
    return front_resistance


def print_optimal_properties(p, resistance):
    print('''
    Number of coils:   {:.4f}
    Inner radius (mm): {:.4f}
    Area sum (m^2):    {:.4f}
    Spacing (mm):      {:.4f}
    Length (mm):       {:.4f}
    Resistance(ohms):  {:.4f}
    '''.format(*p[:2], 1e-6*p[2], *p[3:], resistance))


### BEGIN ###
if __name__ == "__main__":
    

    print(optimal_magnetorquer_front_resistance())
    '''print("Calculating...")

    front_resistance = optimal_magnetorquer_front_resistance()
    inner_resistance = inner_resistance_from_front_resistance(front_resistance)

    out_optimal = find_optimal_spiral(
        front_resistance, outer_layer=True)

    in_optimal = find_optimal_spiral(
        inner_resistance, outer_layer=False)

    total_area_sum = 1e-6*2 * out_optimal[2] + 1e-6*(config.getfloat('NumberOfLayers') - 2) * in_optimal[2]

    print("----Found area-sum maximizing PCB spiral configuration----\n")
    
    print("Outer PCB spiral properties (per spiral):")
    print_optimal_properties(out_optimal, front_resistance)

    print("Inner PCB spiral properties (per spiral):")
    print_optimal_properties(in_optimal, inner_resistance)
    
    print("Total area sum (m^2):  {:.4f}\n".format(total_area_sum))


    KiCad_spiral.save_magnetorquer(
        out_optimal[3], out_optimal[0], out_optimal[3] - config.getfloat("GapBetweenTraces"),
        in_optimal[3], in_optimal[0], in_optimal[3] - config.getfloat("GapBetweenTraces")
    )'''