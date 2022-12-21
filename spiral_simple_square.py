import math
from pathlib import Path
from configparser import ConfigParser
import unittest
from helper_conversions import *
from scipy import optimize

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


def spiral(
    length, spacing, outer_radius=config.getfloat('OuterRadius')
) -> tuple:
    '''
    Returns the sum of coil areas of a square archimedean spiral.
    All else constant, area-sum is proportional to magnetorquer torque.

    Parameters:
        length (float): The length of the spiral's line
        spacing (float): The decrease in radius per 1 turn of rotation
        outer_radius (float): The outer radius of the spiral

    Returns:
        num_of_coils (float): The number of coils in the spiral
        inner_radius (float): The inner radius of the spiral
        area_sum (float): The total area-sum of the spiral
    '''
    r = outer_radius
    s = spacing


    area_sum = -0.5 * spacing * r
    length += spacing

    num_of_coils = 0
    while length > 0:
        num_of_coils += 1
        area_sum += 4 * r ** 2
        length -= 8 * r
        r -= s
        if r < 0:
            return math.nan, math.nan, math.nan
    
    r += s

    area_sum -= -length * r * 0.5

    inner_radius = r
    return area_sum * 1e-6, inner_radius, num_of_coils



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
    upper = 1e6  # TODO: Algorithmatize this hard coded value

    while upper - lower > upper*0.001:

        length_guess = (upper + lower)/2
        s = spacing_from_length(length_guess, resistance, outer_layer)

        if math.isnan(spiral(length_guess, s)[0]):
            upper = length_guess
        else:
            lower = length_guess

    max_length = lower

    return max_length


def spiral_of_resistance(resistance, outer_layer):

    # Dummy function to meet requirements of `optimize.minimize_scalar`
    def neg_area_sum_from_length(length):
        s = spacing_from_length(length, resistance, outer_layer)
        return -spiral(length, s)[0]

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
    return *optimal, spacing, length


class TestSquareSpiral(unittest.TestCase):

    # Square with 2 coils.
    def test_with_two_coils(self):
        result = spiral(16, 0, 1)
        self.assertAlmostEqual(result[0], 8 * 1e-6)
        self.assertAlmostEqual(result[1], 1)
        self.assertAlmostEqual(result[2], 2)

    # Draw it out to confirm!!

    def test_example_spiral_1(self):

        result = spiral(24, 1, 2)
        self.assertAlmostEqual(result[0], 19 * 1e-6)
        self.assertAlmostEqual(result[1], 1)
        self.assertAlmostEqual(result[2], 2)

    # Draw it out to confirm!

    def test_example_spiral_2(self):

        result = spiral(4, 1, 2)
        self.assertAlmostEqual(result[0], 3 * 1e-6)
        self.assertAlmostEqual(result[1], 2)
        self.assertAlmostEqual(result[2], 1)

if __name__ == "__main__":
    unittest.main()