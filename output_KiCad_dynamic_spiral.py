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
                point = point[1], point[0]


    def get_KiCad_text(self, layer):
        out = ""

        if layer % 2 == 1:
            self.flip()
            

        for coil_i in range(len(self.coils)):
            coil = self.coils[coil_i]
            width = self.widths[coil_i]

            out += get_segment(width, get_layer_name(layer), *coil[0], *coil[1])

            for point_i in range(2, len(coil)):
                out += get_segment(width, get_layer_name(layer),
                                    *coil[point_i-1], *coil[point_i])
        
        out += get_segment(1, get_layer_name(layer), *self.coils[-1][-1], config.getfloat("OuterRadius"), config.getfloat("OuterRadius"))

        return out


def get_segment(width, layer, x1, y1, x2, y2):
    net = 0

    return "(segment (start {:.4f} {:.4f}) (end {:.4f} {:.4f}) (width {:.4f}) (layer {}) (net {}))\n".format(
        x1,
        y1,
        x2,
        y2,
        width, layer, net)

def get_via(x, y):
    net = 0
    size = config.getfloat("ViaSize")
    drill = config.getfloat("ViaDrill")

    return f"(via (at {x:.4f} {y:.4f}) (size {size:.4f}) (drill {drill:.4f}) (layers F.Cu B.Cu) (net {net}))\n"


def get_layer_name(layer):
    if layer == 0:
        return 'F.Cu'
    elif layer == config.getint("NumberOfLayers")-1:
        return 'B.Cu'
    else:
        return f"In{layer}.Cu"



def save_spiral(exterior_shape, interior_shape):
    num = config.getint("NumberOfLayers")


    out = exterior_shape.get_KiCad_text(0)

    for i in range(num-2):
        out += interior_shape.get_KiCad_text(i+1)
    
    out += exterior_shape.get_KiCad_text(num-1)

    p = Path(__file__).with_name('KiCad_spiral.txt')
    f = open(p, "w")
    f.write(out)
    f.close()

    print("Saved optimal spiral in KiCad_spiral.txt")
    print("Paste its entire content just before the final closing parantheses of your *.kicad_pcb file")
    print("Save the file, and open KiCad. Your spiral should appear in the PCB editor.")
    
