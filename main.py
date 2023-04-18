from helper_conversions import *
from spiral_simple_square import spiral_of_resistance
from scipy import optimize
import output_KiCad_square_spiral

'''
Main program that outputs an optimized square magnetorquer given
constraints from config.ini
'''

# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


def total_area_sum_from_ext_ohms(ext_ohms: float) -> float:
    '''
    Given the ohms per exterior layer, calculates the area-sum
    of the magnetorquer.

    Parameters:
        ext_ohms (float): the resistance (in ohms) per exterior layer
    Returns:
        - The total area_sum given this constraint

    '''


    int_ohms = int_ohms_from_ext_ohms(ext_ohms)
    int_layers = config.getint("NumberOfLayers") - 2

    area_sum = 2 * spiral_of_resistance(ext_ohms, True)[0]
    area_sum += int_layers * spiral_of_resistance(int_ohms, False)[0]
    return area_sum


def get_optimal_front_resistance() -> float:
    '''
    Find the balance of exterior and interior spiral resistance that
    maximizes area-sum.

    Returns:
        - The optimal resistance per exterior layer spiral
    '''

    front_resistance = optimize.minimize_scalar(
        lambda r: -total_area_sum_from_ext_ohms(r),
        bounds=(0, config.getfloat("Resistance")/2),
        method='bounded'
    ).x

    return front_resistance


def print_about_spiral(spiral, resistance):
    '''
    Helper function to print info about a spiral
    '''

    s = spiral
    print(f'''  Area sum: {s[0]:.4f} m^2
    Inner radius: {s[1]:.4f} mm
    Number of coils: {s[2]:.4f}
    Length of trace: {s[4]:.4f} mm
    Resistance: {resistance:.4f} ohms
    ''')


if __name__ == "__main__":

    # Collect data about the optimal spirals
    ext_ohms = get_optimal_front_resistance()
    int_ohms = int_ohms_from_ext_ohms(ext_ohms)
    exterior = spiral_of_resistance(ext_ohms, True)
    interior = spiral_of_resistance(int_ohms, False)

    # Print information about optimal magnetorquer
    total_area_sum = total_area_sum_from_ext_ohms(ext_ohms)
    print("Optimal properties calculated given config.ini:")
    print(f"Total area-sum: {total_area_sum:.4f} m^2\n")
    print("Properties per each of the 2 external spirals:")
    print_about_spiral(exterior, ext_ohms)
    interior_layers = config.getint("NumberOfLayers") - 2
    print(f"Properties per each of the {interior_layers:d} internal spirals:")
    print_about_spiral(interior, int_ohms)


    # Output the optimal spiral to KiCad_spiral.txt
    output_KiCad_square_spiral.save_magnetorquer(
        exterior[3], exterior[2], interior[3], interior[2])
