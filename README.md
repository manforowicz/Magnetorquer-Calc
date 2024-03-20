# Magnetorquer-Calc
Calculates torque-maximizing properties of a PCB magnetorquer given specific constraints.
Outputs a KiCad text file with the optimized magnetorquer.

## Usage

1. Install scipy with `pip3 install scipy`

2. Modify the magnetorquer constraints in config.ini

3. Run main.py and read the output.

4. Copy the output in KiCad_spiral.txt just before
the final closing parantheses of your *.kicad_pcb file

5. Add through-vias connecting the different spiral layers in KiCad.

6. The simplest way to control your magnetorquer with a microcontroller is to add a 
[DRV8212DRLR](https://www.digikey.com/en/products/detail/texas-instruments/DRV8212DRLR/15286835)
to the circuit board.


## Additional Files

The only scripts invoked for the above operations are
`main.py`, `output_KiCad_square_spiral.py` and `helper_conversions.py`.

The other scripts are simply part of my research to find the optimal magnetorquer design through experimentaiton.

You can learn more about my reserach process by running the `study_*.py` files.
They require the following additional dependencies: matplotlib, numpy. Run `pip3 install matplotlib numpy`

## Real World Applications

I maded a related [video](https://youtu.be/cGJYCe6mGR0) that briefly introduces
how I created a real PCB magnetorquer prototype for Husky Satellite Lab at UW.
