from pathlib import Path
from configparser import ConfigParser


'''
Functions that output a KiCad file of a constant trace width square magnetorquer
'''

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


def get_spiral(spacing, num_of_coils, trace_width, layer) -> str:

    reverse = (layer % 2 == 1)

    outer_radius = config.getfloat("OuterRadius")

    out = ""
    for i in range(num_of_coils):
        radius = outer_radius - i * spacing

        a = (-spacing-radius, -radius)
        b = (radius, -radius)
        c = (radius, radius)
        d = (-radius, radius)
        e = (-radius, spacing-radius)

        out += get_segment(*a, *b, trace_width, layer, reverse)
        out += get_segment(*b, *c, trace_width, layer, reverse)
        out += get_segment(*c, *d, trace_width, layer, reverse)
        out += get_segment(*d, *e, trace_width, layer, reverse)

    return out


def get_segment(x1, y1, x2, y2, width, layer, reverse) -> str:
    net = 0

    offset = config.getfloat("OuterRadius") + 20

    x1 += offset
    y1 += offset
    x2 += offset
    y2 += offset

    if reverse:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if layer == 0:
        layer = 'F.Cu'
    elif layer == config.getint("NumberOfLayers")-1:
        layer = 'B.Cu'
    else:
        layer = f"In{layer}.Cu"

    return f"(segment (start {x1:.4f} {y1:.4f}) (end {x2:.4f} {y2:.4f}) (width {width:.4f}) (layer {layer}) (net {net}))\n"


def save_magnetorquer(exterior_spacing, exterior_num_of_coils,
                      interior_spacing, interior_num_of_coils):
    '''
    Saves the given spiral to "KiCad_spiral.txt".

    Parameters:
        exterior_spacing: Spacing between centers of adjacent traces (in mm) on exterior layers
        exterior_num_of_coils: Number of coils per exterior layer
        interior_spacing: Spacing between centers of adjacent traces (in mm) on interior layers
        interior_num_of_coils: Number of coils per interior layer
    '''

    exterior_width = exterior_spacing - config.getfloat("GapBetweenTraces")
    interior_width = interior_spacing - config.getfloat("GapBetweenTraces")

    num_of_layers = config.getint('NumberOfLayers')

    out = ""

    out += get_spiral(exterior_spacing,
                      exterior_num_of_coils, exterior_width, 0)
    for i in range(num_of_layers-2):
        out += get_spiral(interior_spacing,
                          interior_num_of_coils, interior_width, i+1)

    out += get_spiral(exterior_spacing, exterior_num_of_coils,
                      exterior_width, num_of_layers-1)

    p = Path(__file__).with_name('KiCad_spiral.txt')
    f = open(p, "w")
    f.write(out)
    f.close()

    print("Saved optimal spiral in KiCad_spiral.txt")
    print("Paste its entire content just before the final closing parantheses of your *.kicad_pcb file")
    print("Save the file, and open KiCad. Your spiral should appear in the PCB editor.")
    print("Be sure to add through-vias connecting the different spiral layers.")
