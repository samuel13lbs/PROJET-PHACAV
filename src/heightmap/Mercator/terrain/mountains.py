'''import numpy as np
from noise import pnoise2

def generate_mountains(width, height, scale, seed):
    mountains = np.zeros((height, width))

    for y in range(height):
        for x in range(width):
            n = pnoise2(
                x / scale,
                y / scale,
                octaves=4,
                repeatx=width,
                repeaty=height,
                base=seed
            )
            mountains[y][x] = 1 - abs(n)

    mountains = (mountains - mountains.min()) / (mountains.max() - mountains.min())
    return mountains'''


import numpy as np
from noise import snoise3

def generate_mountains(nx, ny, nz, width, height, scale, seed):
    mountains = np.zeros((height, width))
    
    frequency = 5.0 # Fréquence plus élevée pour les montagnes
    offset = seed + 100 # On décale pour ne pas que les montagnes suivent exactement les continents

    for y in range(height):
        for x in range(width):
            val = snoise3(
                (nx[y, x] * frequency) + offset,
                (ny[y, x] * frequency) + offset,
                (nz[y, x] * frequency) + offset,
                octaves=6, 
                persistence=0.6,
                lacunarity=2.0
            )
           
            mountains[y][x] = 1.0 - abs(val) 

    mountains = (mountains - mountains.min()) / (mountains.max() - mountains.min())
    return mountains