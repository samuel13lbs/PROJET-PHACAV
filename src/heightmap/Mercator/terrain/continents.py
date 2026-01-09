'''import numpy as np
from noise import pnoise2

def generate_continent_mask(width, height, scale, seed):
    mask = np.zeros((height, width))

    for y in range(height):
        for x in range(width):
            mask[y][x] = pnoise2(
                x / scale,
                y / scale,
                octaves=2,
                repeatx=width,
                repeaty=height,
                base=seed
            )

    mask = (mask - mask.min()) / (mask.max() - mask.min())
    return mask'''


import numpy as np
from noise import snoise3

def generate_continent_mask(nx, ny, nz, width, height, scale, seed):
    """ Génère les formes globales des continents """
    mask = np.zeros((height, width))
    
   
    frequency = 2.0  
    
    offset = seed 

    for y in range(height):
        for x in range(width):
           
            val = snoise3(
                (nx[y, x] * frequency) + offset,
                (ny[y, x] * frequency) + offset,
                (nz[y, x] * frequency) + offset,
                octaves=2,
                persistence=0.5,
                lacunarity=2.0
            )
            mask[y][x] = val

    # Normalisation entre 0 et 1
    mask = (mask - mask.min()) / (mask.max() - mask.min())
    
   
    mask[mask < 0.45] = 0.1 
    
    return mask