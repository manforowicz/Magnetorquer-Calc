import math
import numpy as np
from pathlib import Path
from configparser import ConfigParser


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

    def get_KiCad_text(self, layer):
        out = ""

        for coil_i in range(len(self.coils)):
            coil = self.coils[coil_i]
            width = self.widths[coil_i]

            out += get_segment(width, layer, *coil[0], *coil[1])

            for point_i in range(2, len(coil)):
                text += get_segment(width, layer,
                                    coil[point_i-1], coil[point_i])

        return out


def get_segment(width, layer, x1, y1, x2, y2):
    net = 0

    return "(segment (start {:.8f} {:.8f}) (end {:.8f} {:.8f}) (width {:.8f}) (layer {}) (net {}))\n".format(
        x1,
        y1,
        x2,
        y2,
        width, layer, net)


# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']
