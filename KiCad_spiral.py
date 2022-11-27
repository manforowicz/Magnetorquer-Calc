import math
import numpy as np
from pathlib import Path




class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_cartesian_coords(a, b, theta):
    x = (a-b*theta) * math.cos(theta)
    y = (a-b*theta)*math.sin(theta)
    return Point(x, y)


def add_segment(p1, p2, width, layer, net):
    return "(segment (start {:.6f} {:.6f}) (end {:.6f} {:.6f}) (width {:.6f}) (layer {}) (net {}))\n".format(
        p1.x,
        p1.y,
        p2.x,
        p2.y,
        width, layer, net)


def save_curve_kicad(outer_radius, spacing, num_of_coils, stroke_width):
    a = outer_radius
    b = spacing / (2 * math.pi)
    theta = num_of_coils * 2*math.pi

    layer = "F.Cu"
    net = "0"

    p = Path(__file__).with_name('KiCad_spiral.txt')
    f = open(p, "w")

    f.write('''
Paste the following lines somewfweafdfs:
\n\n\n''')
    p1 = get_cartesian_coords(a+5, b, 0)

    for theta in np.arange(0, theta, math.pi/16):
        p2 = get_cartesian_coords(a, b, theta)
        f.write(add_segment(p1, p2, stroke_width, layer, net))
        p1 = p2
    
    f.write(add_segment(p1, Point(0, 0), stroke_width, layer, net))

    f.close()
