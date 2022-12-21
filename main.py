from helper_conversions import *
from spiral_simple_square import spiral_of_resistance
from scipy import optimize
import output_KiCad_square_spiral


def get_total_area_sum_from_front_resistance(front_resistance):
    interior_resistance = interior_resistance_from_front_resistance(front_resistance)
    inner_layers = config.getint("NumberOfLayers") - 2

    area_sum = 0
    area_sum += 2 * spiral_of_resistance(front_resistance, True)[0]
    area_sum += inner_layers * spiral_of_resistance(interior_resistance, False)[0]
    return area_sum

def get_optimal_front_resistance():
    front_resistance = optimize.minimize_scalar(
        lambda r: -get_total_area_sum_from_front_resistance(r),
        bounds=(0, config.getfloat("Resistance")/2),
        method='bounded'
    ).x
    return front_resistance


def get_optimal_magnetorquer():
    front_resistance = get_optimal_front_resistance()
    interior_resistance = interior_resistance_from_front_resistance(front_resistance)

    exterior = spiral_of_resistance(front_resistance, True)
    interior = spiral_of_resistance(interior_resistance, False)

    output_KiCad_square_spiral.save_magnetorquer(exterior[3], exterior[2], interior[3], interior[2])

    


get_optimal_magnetorquer()

print(get_optimal_front_resistance())