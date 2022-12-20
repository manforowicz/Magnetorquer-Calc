from pathlib import Path
from configparser import ConfigParser

'''
Functions 
'''

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


def get_ohms_per_mm(trace_width_mm, exterior_layer):
    '''
    Returns ohms per mm of trace length of given thickness
    '''
    if trace_width_mm <= 0:
        return float("nan")

    thickness_mm = get_trace_thickness(exterior_layer)

    p = config.getfloat("CopperResistivity")

    ohms_per_mm = p / (thickness_mm * trace_width_mm)

    return ohms_per_mm


def get_trace_thickness(exterior_layer):
    '''
    Returns trace thickness in meters
    '''

    if exterior_layer:
        oz_thickness = config.getfloat("OuterLayerThickness")
    else:
        oz_thickness = config.getfloat("InnerLayerThickness")

    m_per_oz = config.getfloat("TraceThicknessPerOz") / 1000

    thickness_m = oz_thickness * m_per_oz

    return thickness_m


def inner_resistance_from_front_resistance(front_resistance):
    return (
        (config.getfloat("Resistance") - 2 * front_resistance) /
        (config.getint("NumberOfLayers") - 2)
    )


def spacing_from_length(length, resistance, exterior):

    thickness_m = get_trace_thickness(exterior)

    coefficient = config.getfloat("CopperResistivity") / thickness_m

    trace_width = length / resistance * coefficient

    return trace_width + config.getfloat("GapBetweenTraces")  # Millimeters
