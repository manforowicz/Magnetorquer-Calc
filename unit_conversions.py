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