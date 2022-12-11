from pathlib import Path
from configparser import ConfigParser

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


def get_ohms_per_mm(trace_width_mm, exterior_layer):
    '''
    Returns ohms per mm of trace length of given thickness
    '''
    if trace_width_mm < 0:
        return float("nan")

    trace_width_m = trace_width_mm / 1000
    thickness_m = get_trace_thickness(exterior_layer)

    p = config.getfloat("CopperResistivity")

    ohms_per_m = p / (thickness_m * trace_width_m)

    ohms_per_mm = ohms_per_m / 1000


    return ohms_per_mm


def get_trace_thickness(exterior_layer):
    '''
    Returns trace thickness in meters
    '''

    if exterior_layer:
        oz_thickness = config.getfloat("OuterLayerThickness")
    else:
        oz_thickness = config.getfloat("InnerLayerThickness")

    thickness_m = (
        oz_thickness 
        * config.getfloat("TraceThicknessPerOz")
        / 1000
    )

    return thickness_m
