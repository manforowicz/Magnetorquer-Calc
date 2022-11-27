import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy import optimize

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


# Returns max trace length physically possible.
# Takes outer radius and a function that defines spacing
def max_trace_length(outer_radius, spacing_from_length):

    def inner_radius_from_length(length):
        s = spacing_from_length(length)
        return properties_of_spiral(outer_radius, length, s)[1]

    return optimize.brentq(inner_radius_from_length, 0, 1e9)


# Takes spiral properties:
# - outer_radius: radius of outer coil
# - length: total length of the spiral
# - spacing: distance between centers of adjacent coils
#
# Returns: Number of coils, inner radius of spiral, sum of coil areas
def properties_of_spiral(outer_radius, length, spacing):
    a = outer_radius
    b = spacing / (2 * math.pi)

    if b == 0:  # If b is 0 we have a perfect circle
        theta = length / outer_radius  # Circle arc length formula
    else:
        # a/b gives theta that results in 0 inner radius
        # If user gives a greater length, use that (even though it physically won't fit)
        max_theta = max(length, a/b)

        # Use math to find theta that gives a spiral of the desired length
        theta = optimize.brentq(
            lambda t: length_of_spiral(a, b, t) - length, 0, max_theta)

    # Calculate and return other properties from theta
    num_of_coils = theta / (2 * math.pi)
    inner_radius = a - b*theta
    area_sum = area_sum_of_spiral(a, b, theta)

    return num_of_coils, inner_radius, area_sum


# Finds trace length tha maximizes area-sum
def find_max_area_sum():

    # Dummy function to meet requirements of `optimize.minimize_scalar`
    def neg_area_sum_from_length(length):
        s = spacing_from_length(length)
        return -properties_of_spiral(OUTER_RADIUS, length, s)[2]

    max_length = max_trace_length(OUTER_RADIUS, spacing_from_length)
    # Finds length that gives maximum area-sum
    length = optimize.minimize_scalar(
        neg_area_sum_from_length,
        bounds=(0, max_length),
        method='bounded'
    ).x

    # Calculate data from the optimal length
    spacing = spacing_from_length(length)
    optimal = properties_of_spiral(OUTER_RADIUS, length, spacing)

    KiCad_spiral.save_curve_kicad(OUTER_RADIUS*10, spacing*10, optimal[0], (spacing-GAP_BETWEEN_TRACE_EDGES)*10)
    print("Saved optimzed spiral SVG to current directory.\n")

    # Print data
    print(
        "--- The following length maximizes the area sum of coils. ---\n")
    print(
        "Length of trace (cm):                        {:.4f}\n".format(length))
    print(
        "Center-to-center spacing between coils (cm): {:.4f}\n".format(spacing))
    print(
        "Inner radius (cm):                           {:.4f}\n".format(optimal[1]))
    print(
        "Inner radius / Outer radius:                 {:.4f}\n".format(optimal[1] / OUTER_RADIUS))
    print(
        "Number of coils (#):                         {:.4f}\n".format(optimal[0]))
    print(
        "Area sum of coils (cm^2):                    {:.4f}\n".format(optimal[2]))

    

# Draws a nice little graph
def draw_graph():
    length_array = []
    area_sum_array = []

    max_length = max_trace_length(OUTER_RADIUS, spacing_from_length)
    for length in np.linspace(0, max_length, 50):

        spacing = spacing_from_length(length)
        area_sum = properties_of_spiral(OUTER_RADIUS, length, spacing)[2]

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


### TWEAKABLES ####

# Define this function to return spacing that ensures resistance stays constant given length
def spacing_from_length(length):
    trace_width = length / DESIRED_RESISTANCE * 5.086e-4
    return trace_width + GAP_BETWEEN_TRACE_EDGES  # centimeters


# Centimeters
OUTER_RADIUS = 4

# OHMS (Note: If both front and back of PCB is used, total resistance doubles)
DESIRED_RESISTANCE = 10

# Centimeters
GAP_BETWEEN_TRACE_EDGES = 0.013

### BEGIN ###
if __name__ == "__main__":
    test_func_properties_of_spiral()
    find_max_area_sum()
    draw_graph()
