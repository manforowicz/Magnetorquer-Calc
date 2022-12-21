from pathlib import Path
import numpy as np
import math

#### NOTES ####
# This is only a helper program that outputs an SVG file
# It is used to draw an optimized spiral from a different program


# Stores a simple point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Get coordinates at theta of given spiral
def get_cartesian_coords(a, b, theta):
    x = (a-b*theta) * math.cos(theta)
    y = (a-b*theta)*math.sin(theta)
    return Point(x, y)


# Get slope at theta of given spiral
def get_cartesian_slope(a, b, theta):
    return (
        (-b*math.sin(theta) + (a-b*theta)*math.cos(theta)) /
        (-b*math.cos(theta) + (a-b*theta)*-math.sin(theta))
    )


# Finds intersection of 2 point-slope lines
def find_intersection(m1, p1, m2, p2):
    x = (m1*p1.x - p1.y - m2*p2.x + p2.y) / (m1 - m2)
    y = m1*(x - p1.x) + p1.y
    return Point(x, y)


# Draws a quadratic bezier curve
def curve(handle, endpoint):
    return "Q {:.4f} {:.4f}, {:.4f} {:.4f}\n".format(handle.x, handle.y, endpoint.x, endpoint.y)


#Draw an svg spiral and save it to the current directory
def save_curve_svg(outer_radius, spacing, num_of_coils, stroke_width):
    a = outer_radius
    b = spacing / (2 * math.pi)
    theta = num_of_coils * 2*math.pi

    p = Path(__file__).with_name('spiral.svg')
    f = open(p, "w")
    f.write('''<svg
        width = "{0:.4f}cm"
        height = "{0:.4f}cm"
        viewBox = "{1:.4f} {1:.4f} {0:.4f} {0:.4f}"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:svg="http://www.w3.org/2000/svg">\n'''.format(outer_radius*2, -outer_radius))

    f.write('''<path style="fill:none; stroke:#000000; stroke-width:{};"\n'''.format(stroke_width))
    f.write('d="')

    m1 = get_cartesian_slope(a, b, 0)
    p1 = get_cartesian_coords(a, b, 0)
    f.write("M {:.4f} {:.4f}\n".format(p1.x, p1.y))

    for theta in np.arange(math.pi/4, theta, math.pi/4):
        m2 = get_cartesian_slope(a, b, theta)
        p2 = get_cartesian_coords(a, b, theta)
        i = find_intersection(m1, p1, m2, p2)
        f.write(curve(i, p2))
        m1, p1 = m2, p2

    # Closing
    f.write('''"/>
    </svg>''')
    f.close()
