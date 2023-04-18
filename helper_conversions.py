from pathlib import Path
from configparser import ConfigParser

'''
Helper Conversion Functions
'''

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


def get_ohms_per_mm(trace_width_mm: float, exterior_layer: bool) -> float:
    '''
    Parameters:
        - Width of PCB trace in mm
        - Boolean whether the trace is on PCB exterior layer
    Returns: ohms per mm of trace length
    '''
    if trace_width_mm <= 0:
        return float("nan")

    thickness_m = get_trace_thickness(exterior_layer)

    p = config.getfloat("CopperResistivity")

    ohms_per_mm = p / (thickness_m * trace_width_mm)

    return ohms_per_mm


def get_trace_thickness(exterior_layer: bool) -> float:
    '''
    Parameters:
        - Boolean whether the trace is on PCB exterior layer
    Returns: Thickness of trace (in meters)
    '''
    if exterior_layer:
        oz_thickness = config.getfloat("OuterLayerThickness")
    else:
        oz_thickness = config.getfloat("InnerLayerThickness")

    m_per_oz = config.getfloat("TraceThicknessPerOz") / 1000

    thickness_m = oz_thickness * m_per_oz

    return thickness_m


def int_ohms_from_ext_ohms(exterior_resistance: float) -> float:
    '''
    Parameters:
        - Resistance per spiral on the exterior layer
    Returns: Resistance (in ohms) per inner spiral required to meet total resistance config
    '''
    return (
        (config.getfloat("Resistance") - 2 * exterior_resistance) /
        (config.getint("NumberOfLayers") - 2)
    )


def spacing_from_length(length_mm: float, resistance: float, exterior: bool) -> float:
    '''
    Parameters:
        - Length of trace in mm
        - Desired resistance in ohms
        - Boolean whether the trace is on PCB exterior
    Returns: Total spacing (in mm) between centers of adjacent traces
    '''
    thickness_m = get_trace_thickness(exterior)

    p = config.getfloat("CopperResistivity")

    trace_width_mm = (p * length_mm) / (thickness_m * resistance)

    return trace_width_mm + config.getfloat("GapBetweenTraces")
