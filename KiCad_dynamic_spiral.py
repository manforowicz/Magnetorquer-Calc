import math
import numpy as np
from pathlib import Path
from configparser import ConfigParser


# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def get_square(outer_radius, radius, outer_spacing, inner_spacing, clockwise: bool, width, layer):
    o_r = outer_radius
    r = radius


def segment(p1, p2, width, layer, net):
    return "(segment (start {:.8f} {:.8f}) (end {:.8f} {:.8f}) (width {:.8f}) (layer {}) (net {}))\n".format(
        p1.x,
        p1.y,
        p2.x,
        p2.y,
        width, layer, net)