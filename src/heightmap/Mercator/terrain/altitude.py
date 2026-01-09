'''import numpy as np
from terrain.continents import generate_continent_mask
from terrain.mountains import generate_mountains
from terrain.ridges import generate_ridges
from noise import pnoise2

def generate_base_altitude(width, height, scale, seed):
    base = np.zeros((height, width))

    for y in range(height):
        for x in range(width):
            base[y][x] = pnoise2(
                x / scale,
                y / scale,
                octaves=6,
                repeatx=width,
                repeaty=height,
                base=seed
            )

    base = (base - base.min()) / (base.max() - base.min())
    return base


def generate_altitude_map(config):
    width = config["width"]
    height = config["height"]
    seed = config["seed"]

    continent_mask = generate_continent_mask(
        width, height, config["continent_scale"], seed
    )

    base_altitude = generate_base_altitude(
        width, height, config["base_scale"], seed
    )

    mountains = generate_mountains(
        width, height, config["mountain_scale"], seed + 1
    )

    ridges = generate_ridges(width, height)

    altitude = base_altitude * continent_mask
    altitude += mountains * config["mountain_strength"] * continent_mask
    altitude += ridges * config["ridge_strength"] * (1 - continent_mask)

    altitude = (altitude - altitude.min()) / (altitude.max() - altitude.min())
    return altitude'''

import numpy as np
from terrain.projection import get_3d_coordinates
from terrain.continents import generate_continent_mask
from terrain.mountains import generate_mountains

def generate_altitude_map(config):
    width = config["width"]
    height = config["height"]
    seed = config["seed"]

    print("1. Calcul de la projection sphérique...")
   
    nx, ny, nz = get_3d_coordinates(width, height)

    print("2. Génération des continents...")
    continent_mask = generate_continent_mask(
        nx, ny, nz, width, height, config["continent_scale"], seed
    )

    print("3. Génération des montagnes...")
    mountains = generate_mountains(
        nx, ny, nz, width, height, config["mountain_scale"], seed
    )

   
    altitude = continent_mask * 0.5 
    
    
    altitude += mountains * config["mountain_strength"] * (continent_mask > 0.2)

   
    altitude = (altitude - altitude.min()) / (altitude.max() - altitude.min())
    
    return altitude
    base = (base -base.min()) / (base.max() - base.min())
    return base