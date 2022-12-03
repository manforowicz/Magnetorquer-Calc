import math
from scipy import integrate
from scipy import optimize
from pathlib import Path
import configparser
import unittest

'''
Helper functions that calculate geometric properties of spirals
'''

# Read configuration
config = configparser.ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


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


def properties_of_round_spiral(
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
    area_sum = area_sum_of_round_spiral(a, b, theta)

    return num_of_coils, inner_radius, area_sum


def area_added_by_edge(radius):
    '''
    Returns the area added by drawing an edge on a square spiral.

    Parameters:
        radius (float): The radius of the edge from the spiral's center

    Returns:
        area (float): Area added by drawing this edge on a square spiral
    '''

    return radius ** 2


def properties_of_square_spiral(
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
    num_of_coils = 0

    # Draw one additional outer edge
    length -= r*2
    area_sum = area_added_by_edge(r)

    # Draw spiral, going 2 edges at a time.
    if length > 0:
        r += s/2
    while length > 0:
        r -= s/2
        if r < 0:
            return math.nan, math.nan, math.nan

        length -= 4*r
        area_sum += 2 * area_added_by_edge(r)
        num_of_coils += 0.5

    # If overshot by more than one edge, remove that edge
    if length < -2*r:
        area_sum -= area_added_by_edge(r)
        length += 2*r
        num_of_coils -= 0.5

    # Remove triangle area of overshot length
    area_sum -= -length * r / 2

    # Calculate other properties
    inner_radius = r

    return num_of_coils, inner_radius, area_sum



#### TESTS ####

class TestRoundSpiral(unittest.TestCase):

    # Circle with 2 coils.
    def test_circle_with_two_coils(self):
        result = properties_of_round_spiral(4 * math.pi, 0, 1)
        self.assertAlmostEqual(result[0], 2)
        self.assertAlmostEqual(result[1], 1)
        self.assertAlmostEqual(result[2], 2 * math.pi)

    # Compare with results received from https://planetcalc.com/9063/

    def test_more_complicated_spiral(self):
        result = properties_of_round_spiral(100, 1, 10)
        self.assertAlmostEqual(result[0], 1.7432534773931)
        self.assertAlmostEqual(result[1], 8.25674652261)
        # self-calculated. (question validity)
        self.assertAlmostEqual(result[2], 457.73601090254937)


class TestSquareSpiral(unittest.TestCase):

    # Square with 2 coils.
    def test_square_with_two_coils(self):
        result = properties_of_square_spiral(16, 0, 1)
        self.assertAlmostEqual(result[0], 2)
        self.assertAlmostEqual(result[1], 1)
        self.assertAlmostEqual(result[2], 8)

    # Draw it out to confirm!!

    def test_example_spiral_1(self):

        result = properties_of_square_spiral(24, 1, 2)
        self.assertAlmostEqual(result[0], 2)
        self.assertAlmostEqual(result[1], 0.5)
        self.assertAlmostEqual(result[2], 19)


if __name__ == '__main__':
    unittest.main()
