import math
import numpy as np
from scipy import optimize
from pathlib import Path
import configparser
from spirals import properties_of_square_spiral
import KiCad_spiral

'''
Goal is to find coil that maximizes area-sum under the given constraints
Area-sum is the sum of the areas created by each coil
Assuming everything else is constant, area-sum is proportional to magnetorquer's torque

Spiral used is a square spiral similar to an archimedean spiral
This spiral is used due to its favorable characteristics demonstrated in square_vs_circle.py
'''


# Read configuration
config = configparser.ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']



# Returns spacing of trace needed to give desired resistance
def spacing_from_length(length, resistance, outer_layer):
    if outer_layer:
        thickness_in_oz = config.getfloat("OuterLayerThickness")
    else:
        thickness_in_oz = config.getfloat("InnerLayerThickness")

    thickness_in_m = thickness_in_oz * \
        config.getfloat("TraceThicknessPerOz")/1000

    coefficient = config.getfloat("CopperResistivity") / thickness_in_m

    trace_width = length / resistance * coefficient

    return trace_width + config.getfloat("GapBetweenTraces")  # Millimeters


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
        max_length: Maximum length of wire that can fit on the spiral.

    '''
    lower = 0
    upper = 1e6

    while upper - lower > upper*0.001:
        
        length_guess = (upper + lower)/2
        s = spacing_from_length(length_guess, resistance, outer_layer)
        
        if math.isnan(properties_of_square_spiral(length_guess, s)[0]):
            upper = length_guess
        else:
            lower = length_guess
    
    max_length = lower
    return max_length


# Finds trace length tha maximizes area-sum
def find_optimal_spiral(resistance, outer_layer):

    # Dummy function to meet requirements of `optimize.minimize_scalar`
    def neg_area_sum_from_length(length):
        s = spacing_from_length(length, resistance, outer_layer)
        return -properties_of_square_spiral(length, s)[2]

    max_length = max_trace_length(resistance, outer_layer)
    # Finds length that gives maximum area-sum
    length = optimize.minimize_scalar(
        neg_area_sum_from_length,
        bounds=(0, max_length),
        method='bounded'
    ).x

    # Calculate data from the optimal length
    spacing = spacing_from_length(length, resistance, outer_layer)
    optimal = properties_of_square_spiral(length, spacing)

    # Return coil spacing, number of coils, and area-sum
    return spacing, optimal[0], optimal[2]


def inner_resistance_from_front_resistance(front_resistance):
    return (
        (config.getfloat("Resistance") - 2 * front_resistance) /
        (config.getint("NumberOfLayers") - 2)
    )


def find_total_area_sum_from_front_resistance(front_resistance):
    inner_resistance = inner_resistance_from_front_resistance(front_resistance)
    inner_layers = config.getint("NumberOfLayers") - 2

    area_sum = 0
    area_sum += 2 * find_optimal_spiral(front_resistance, True)[2]
    area_sum += inner_layers * find_optimal_spiral(inner_resistance, False)[2]
    return area_sum


def optimal_magnetorquer_front_resistance():
    front_resistance = optimize.minimize_scalar(
        lambda r: -find_total_area_sum_from_front_resistance(r),
        bounds=(0, config.getfloat("Resistance")/2),
        method='bounded'
    ).x
    return front_resistance



### BEGIN ###
if __name__ == "__main__":
    print("Calculating...")
    # test_func_properties_of_spiral()
    #find_optimal_spiral(config.getfloat('Resistance'), True)

    front_resistance = optimal_magnetorquer_front_resistance()
    inner_resistance = inner_resistance_from_front_resistance(front_resistance)
    
    out_spacing, out_num_of_coils, _ = find_optimal_spiral(
        front_resistance, True)
    
    in_spacing, in_num_of_coils, _ = find_optimal_spiral(
        inner_resistance, False)


    KiCad_spiral.save_magnetorquer(config.getint("NumberOfLayers"), config.getfloat("OuterRadius"),
                                   out_spacing, out_num_of_coils, out_spacing -
                                   config.getfloat("GapBetweenTraces"),
                                   in_spacing, in_num_of_coils, in_spacing - config.getfloat("GapBetweenTraces"))
    

