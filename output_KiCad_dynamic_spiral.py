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


class SpiralShape:
    def __init__(self):
        self.coils = []
        self.widths = []

    def add_coil(self, width, *args):
        self.coils.append([*args])
        self.widths.append(width)
    
    def flip(self):
        for coil in self.coils:
            for point in coil:
                point[1], point[0] = point[0], point[1]


    def get_KiCad_text(self, layer):
        out = ""

        if layer % 2 == 1:
            self.flip()
            

        for coil_i in range(len(self.coils)):
            coil = self.coils[coil_i]
            width = self.widths[coil_i]

            out += get_segment(width, layer, *coil[0], *coil[1])

            for point_i in range(2, len(coil)):
                out += get_segment(width, get_layer_name(layer),
                                    coil[point_i-1], coil[point_i])
        
        out += get_segment(*self.coils[-1][-1], config.getfloat("OuterRadius"), config.getfloat("OuterRadius"))

        return out


def get_segment(width, layer, x1, y1, x2, y2):
    net = 0

    return "(segment (start {:.8f} {:.8f}) (end {:.8f} {:.8f}) (width {:.8f}) (layer {}) (net {}))\n".format(
        x1,
        y1,
        x2,
        y2,
        width, layer, net)

def get_via(x, y, layer1, layer2):
    net = 0
    layer1 = get_layer_name(layer1)
    layer2 = get_layer_name(layer2)
    size = config.getfloat("ViaSize")
    drill = config.getfloat("ViaDrill")

    return f"(via (at {x} {y}) (size {size}) (drill {drill}) (layers {layer1} {layer2}) (net {net}))"


def get_layer_name(layer):
    if layer == 0:
        return 'F.Cu'
    elif layer == config.getint("NumberOfLayers"):
        return 'B.Cu'
    else:
        return f"In{layer}.Cu"



def save_spiral(exterior_shape, interior_shape):
    num = config.getint("NumberOfLayers")
    outer_radius = config.getfloat("OuterRadius")


    out = exterior_shape.get_KiCad_text(0)

    out += get_via(outer_radius, outer_radius, 0, 1)

    for i in range(num-2):
        out += interior_shape.get_KiCadText(i+1)
        out += get_via(0, 0, i+1, i+2)
    
    out += exterior_shape.get_KiCad_text(num-1)

    p = Path(__file__).with_name('KiCad_spiral.txt')
    f = open(p, "w")
    f.write(out)
    f.close()

    print("Saved optimal spiral in KiCad_spiral.txt")
    print("Paste its entire content just before the final closing parantheses of your *.kicad_pcb file")
    print("Save the file, and open KiCad. Your spiral should appear in the PCB editor.")
    
