import math
import numpy as np
from pathlib import Path


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_cartesian_coords(a, b, theta):
    x = (a-b*abs(theta)) * math.cos(theta)
    y = (a-b*abs(theta)) * math.sin(theta)
    return Point(x, y)


def add_segment(p1, p2, width, layer, net):
    return "(segment (start {:.6f} {:.6f}) (end {:.6f} {:.6f}) (width {:.6f}) (layer {}) (net {}))\n".format(
        p1.x,
        p1.y,
        p2.x,
        p2.y,
        width, layer, net)


def get_spiral(outer_radius, spacing, num_of_coils, stroke_width, layer, reverse):
    a = outer_radius
    b = spacing / (2 * math.pi)
    theta = num_of_coils * 2*math.pi

    net = "0"

    text = ""

    p1 = get_cartesian_coords(a+5, b, 0)

    for theta in np.arange(0, theta, math.pi/16):
        if reverse:
            theta *= -1
        p2 = get_cartesian_coords(a, b, theta)
        text += add_segment(p1, p2, stroke_width, layer, net)
        p1 = p2

    text += add_segment(p1, Point(0, 0), stroke_width, layer, net)

    return text


def save_magnetorquer(num_of_layers, outer_radius,
                      out_spacing, out_num_of_coils, out_stroke_width,
                      in_spacing, in_num_of_coils, in_stroke_width):
    p = Path(__file__).with_name('KiCad_spiral.txt')
    f = open(p, "w")

    step = math.pi/16
    f.write(get_spiral(outer_radius, out_spacing,
            out_num_of_coils, out_stroke_width, "F.Cu", False))

    for i in range(num_of_layers - 2):
        layer = "In" + str(i+1) + ".Cu"
        f.write(get_spiral(outer_radius, in_spacing,
                in_num_of_coils, in_stroke_width, layer, i % 2 == 0))

    f.write(get_spiral(outer_radius, out_spacing,
            out_num_of_coils, out_stroke_width, "B.Cu", num_of_layers % 2 == 0))

    f.close()
