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


def get_half(outer_radius, radius, side: bool, spacing, width, layer):
    o_r = outer_radius
    r = radius

    if side:
        p1 = Point(o_r - r, o_r - r)
        p3 = Point(o_r + r - spacing/2, o_r + r - spacing/2)
    else:
        p1 = Point(o_r - r + spacing/2, o_r - r + spacing/2)
        p3 = Point(o_r + r, o_r + r)

    if side:
        p2 = Point(p1.x, p3.y)
    else:
        p2 = Point(p3.x, p1.y)

    return segment(p1, p2, width, layer, "0") + segment(p2, p3, width, layer, "0")


def segment(p1, p2, width, layer, net):
    return "(segment (start {:.8f} {:.8f}) (end {:.8f} {:.8f}) (width {:.8f}) (layer {}) (net {}))\n".format(
        p1.x,
        p1.y,
        p2.x,
        p2.y,
        width, layer, net)


def get_spiral(spacing, num_of_coils, stroke_width, layer, reverse):

    r = outer_radius = config.getfloat('OuterRadius')
    text = ""

    # Draw spiral, going 2 edges at a time.
    for i in range(2*int(num_of_coils)):

        text += get_half(outer_radius, r, reverse,
                         spacing, stroke_width, layer)

        r -= spacing/2
        reverse = not reverse

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
