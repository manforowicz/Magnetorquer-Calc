import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy import optimize
from pathlib import Path
import configparser

import KiCad_spiral

#### NOTES ####
# Goal is to find coil that maximizes area-sum under the given constraints
# Area-sum is the sum of the areas created by each coil
# Assuming everything else is constant, area-sum is proportional to magnetorquer's torque

# Spiral used is an archimedean spiral due to its constant spacing between coils
# Its equation is r = a - b*theta (where `a` is the outer radius, and `b` is decrease of radius per radian)
# Any variables named a and b are referring to the coefficients in this equation


#### HELPER FUNCTIONS ####

# Returns length of spiral. Proof: https://planetcalc.com/3707/
def length_of_spiral(a, b, theta):
    return integrate.quad(lambda t: math.sqrt((a - b*t)**2 + b**2), 0, theta)[0]


# Returns sum of coil areas
def area_sum_of_spiral(a, b, theta):
    return integrate.quad(lambda t: 0.5*(a - b*t)**2, 0, theta)[0]


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

    def inner_radius_from_length(length):
        s = spacing_from_length(length, resistance, outer_layer)
        return properties_of_spiral(length, s)[1]

    return optimize.brentq(inner_radius_from_length, 0, 1e9)


# Takes spiral properties:
# - outer_radius: radius of outer coil
# - length: total length of the spiral
# - spacing: distance between centers of adjacent coils
#
# Returns: Number of coils, inner radius of spiral, sum of coil areas
def properties_of_spiral(length, spacing):

    a = config.getfloat("OuterRadius")
    b = spacing / (2 * math.pi)

    if b == 0:  # If b is 0 we have a perfect circle
        theta = length / a  # Circle arc length formula
    else:
        # a/b gives theta that results in 0 inner radius
        # If user gives a greater length, use that (even though it physically won't fit)
        max_theta = max(length/b, a/b)

        # Use math to find theta that gives a spiral of the desired length
        theta = optimize.brentq(
            lambda t: length_of_spiral(a, b, t) - length, 0, max_theta)

    # Calculate and return other properties from theta
    num_of_coils = theta / (2 * math.pi)
    inner_radius = a - b*theta
    area_sum = area_sum_of_spiral(a, b, theta)

    return num_of_coils, inner_radius, area_sum


# Finds trace length tha maximizes area-sum
def find_optimal_spiral(resistance, outer_layer):

    # Dummy function to meet requirements of `optimize.minimize_scalar`
    def neg_area_sum_from_length(length):
        s = spacing_from_length(length, resistance, outer_layer)
        return -properties_of_spiral(length, s)[2]

    max_length = max_trace_length(resistance, outer_layer)
    # Finds length that gives maximum area-sum
    length = optimize.minimize_scalar(
        neg_area_sum_from_length,
        bounds=(0, max_length),
        method='bounded'
    ).x

    # Calculate data from the optimal length
    spacing = spacing_from_length(length, resistance, outer_layer)
    optimal = properties_of_spiral(length, spacing)

    # Return coil spacing, number of coils, and area-sum
    return spacing, optimal[0], optimal[2]


def inner_resistance_from_front_resistance(front_resistance):
    return (
            (config.getfloat("Resistance") - 2 * front_resistance) /
            (config.getint("NumberOfLayers") - 2)
            )


def find_total_area_sum_from_front_resistance(front_resistance):
    inner_resistance = inner_resistance_from_front_resistance(front_resistance)
    inner_layers = config.getint("NumberOfLayers") -2

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
    


'''
# Draws a nice little graph
def draw_graph():
    length_array = []
    area_sum_array = []

    max_length = max_trace_length(config.getfloat('resistance'), True)
    for length in np.linspace(0, max_length, 50):

        spacing = spacing_from_length(length, config.getfloat('resistance'), True)
        area_sum = properties_of_spiral(length, spacing)[2]

        length_array.append(length)
        area_sum_array.append(area_sum)

    plt.plot(length_array, area_sum_array, "-o")
    plt.xlabel("Length of PCB trace (cm)")
    plt.ylabel("Sum of coil areas (cm^2)")
    plt.show()



def test_func_properties_of_spiral():
    # Circle with 2 coils.
    result = properties_of_spiral(1, 4 * math.pi, 0)
    assert abs(result[0] - 2) < 0.001
    assert abs(result[1] - 1) < 0.001
    assert abs(result[2] - 2 * math.pi) < 0.001

    # Compare with results received from https://planetcalc.com/9063/
    result = properties_of_spiral(10, 100, 1)
    assert abs(result[0] - 1.7433) < 0.001
    assert abs(result[1] - 8.2568) < 0.001

    print("All tests passed!\n")
'''


# Read configuration
config = configparser.ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']

### BEGIN ###
if __name__ == "__main__":
    print("Calculating...")
    # test_func_properties_of_spiral()
    #find_optimal_spiral(config.getfloat('Resistance'), True)

    front_resistance = optimal_magnetorquer_front_resistance()
    inner_resistance = inner_resistance_from_front_resistance(front_resistance)
    out_spacing, out_num_of_coils, _ = find_optimal_spiral(front_resistance, True)
    in_spacing, in_num_of_coils, _ = find_optimal_spiral(inner_resistance, False)

    KiCad_spiral.save_magnetorquer(config.getint("NumberOfLayers"), config.getfloat("OuterRadius"),
                        out_spacing, out_num_of_coils, out_spacing - config.getfloat("GapBetweenTraces"),
                        in_spacing, in_num_of_coils, in_spacing - config.getfloat("GapBetweenTraces"))


