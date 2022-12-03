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


def get_cartesian_coords(a, b, theta):
    x = (a-b*abs(theta)) * math.cos(theta)
    y = (a-b*abs(theta)) * math.sin(theta)
    return Point(x, y)

def add_spiral_segment(r, side):
    '''
    side: 0up 1right 2down 3right
    '''
    if side == 0:
        


def add_segment(p1, p2, width, layer, net):
    return "(segment (start {:.6f} {:.6f}) (end {:.6f} {:.6f}) (width {:.6f}) (layer {}) (net {}))\n".format(
        p1.x,
        p1.y,
        p2.x,
        p2.y,
        width, layer, net)


def get_spiral(spacing, num_of_coils, stroke_width, layer, reverse):

    r = config.getfloat('OuterRadius')
    s = spacing
    net = "0"
    text = ""


    # Draw one additional outer edge
    num_of_coils = 0.25

    # Draw spiral, going 2 edges at a time.
    for i in range(2*int(num_of_coils)):
        
        
        r -= s/2

    

    p1 = get_cartesian_coords(a+5, b, 0)

    text += add_segment(p1, Point(0, 0), stroke_width, layer, net)

    return text


def save_magnetorquer(out_spacing, out_num_of_coils, out_stroke_width,
                      in_spacing, in_num_of_coils, in_stroke_width):
    p = Path(__file__).with_name('KiCad_spiral.txt')
    f = open(p, "w")

    num_of_layers = config.getint('NumberOfLayers')

    f.write(get_spiral(out_spacing,
            out_num_of_coils, out_stroke_width, "F.Cu", False))

    for i in range(num_of_layers - 2):
        layer = "In" + str(i+1) + ".Cu"
        f.write(get_spiral(in_spacing,
                in_num_of_coils, in_stroke_width, layer, i % 2 == 0))

    f.write(get_spiral(out_spacing,
            out_num_of_coils, out_stroke_width, "B.Cu", num_of_layers % 2 == 0))

    f.close()

    print("Saved optimal spiral in KiCad_spiral.txt")
    print("Paste its entire content just before the final closing parantheses of your *.kicad_pcb file")
    print("Save the file, and open KiCad. Your spiral should appear in the PCB editor.")