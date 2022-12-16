import math
import numpy as np
from pathlib import Path
from configparser import ConfigParser


# Read configuration
config = ConfigParser()
config.read(Path(__file__).with_name('config.ini'))
config = config['Configuration']


def save_spiral()