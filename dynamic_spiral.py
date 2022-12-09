import math
from scipy import integrate
from scipy import optimize
from pathlib import Path
from configparser import ConfigParser
import unittest

'''
Helper functions that calculate geometric properties of dynamic spirals
'''

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']

def spiral(outer_radius, length_width_ratio):
    r = outer_radius

    area_sum = 0

    area_sum += r**2