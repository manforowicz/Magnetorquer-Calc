import math
from scipy import integrate
from scipy import optimize
from pathlib import Path
from configparser import ConfigParser
import unittest
from unit_conversions import *

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']

#### ROUND FUNCTIONS ####


def length_of_round_spiral(a: float, b: float, theta: float) -> float:
    '''
    Returns the length of a circular archimedean spiral.
    Proof: https://planetcalc.com/3707/

    Parameters:
        a (float): The outer radius of the spiral
        b (float): The decrease in radius per 1 radian of rotation
        theta (float): The number of radians

    Returns:
        Length (float): The length of the spiral
    '''
    return integrate.quad(lambda t: math.sqrt((a - b*t)**2 + b**2), 0, theta)[0]


def area_sum_of_round_spiral(a: float, b: float, theta: float) -> float:
    '''
    Returns the sum of coil areas of a circular archimedean spiral.
    All else constant, area-sum is proportional to magnetorquer torque.

    Parameters:
        a (float): The outer radius of the spiral
        b (float): The decrease in radius per 1 radian of rotation
        theta (float): The number of radians

    Returns:
        Area-sum (float): The area-sum of the spiral
    '''
    return integrate.quad(lambda t: 0.5*(a - b*t)**2, 0, theta)[0]


def spiral(
    length, spacing, outer_radius=config.getfloat('OuterRadius')
) -> tuple:
    '''
    Returns the sum of coil areas of a circular archimedean spiral.
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
    a = outer_radius
    b = spacing / (2 * math.pi)

    if b == 0:  # If b is 0 we have a perfect circle
        theta = length / a  # Circle arc length formula
    else:
        # a/b gives theta that results in 0 inner radius
        max_theta = a / b

        # If user gives a longer length, that won't fit, so return NaN
        if length > length_of_round_spiral(a, b, max_theta):
            return math.nan, math.nan, math.nan

        # Use math to find theta that gives a spiral of the desired length
        theta = optimize.brentq(
            lambda t: length_of_round_spiral(a, b, t) - length, 0, max_theta)

    # Calculate and return other properties from theta
    num_of_coils = theta / (2 * math.pi)
    inner_radius = a - b*theta
    area_sum = area_sum_of_round_spiral(a, b, theta) * 10e-6

    return area_sum, inner_radius, num_of_coils

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

class TestRoundSpiral(unittest.TestCase):

    # Circle with 2 coils.
    def test_with_two_coils(self):
        result = spiral(4 * math.pi, 0, 1)
        self.assertAlmostEqual(result[0], 2)
        self.assertAlmostEqual(result[1], 1)
        self.assertAlmostEqual(result[2], 2 * math.pi)

    # Compare with results received from https://planetcalc.com/9063/

    def test_example_1(self):
        result = spiral(100, 1, 10)
        self.assertAlmostEqual(result[0], 1.7432534773931)
        self.assertAlmostEqual(result[1], 8.25674652261)

        # self-calculated. (question validity)
        self.assertAlmostEqual(result[2], 457.73601090254937)