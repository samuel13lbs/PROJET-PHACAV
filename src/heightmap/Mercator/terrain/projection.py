'''import numpy as np

def spherical_to_2d(height, width):
    """
    Retourne deux matrices :
    latitude[y][x]  ∈ [-π/2, π/2]
    longitude[y][x] ∈ [-π, π]
    """

    latitudes = np.zeros((height, width))
    longitudes = np.zeros((height, width))

    for y in range(height):
        lat = np.pi * (0.5 - y / height)
        for x in range(width):
            lon = 2 * np.pi * (x / width - 0.5)
            latitudes[y][x] = lat
            longitudes[y][x] = lon

    return latitudes, longitudes'''


import numpy as np
import math

def get_3d_coordinates(width, height):
   
    xs = np.linspace(0, 1, width)
    ys = np.linspace(0, 1, height)
    
    
    lon_vals, lat_vals = np.meshgrid(xs, ys)

    # Conversion Mercator -> Sphère 3D
    # Longitude : 0 à 2*PI (tour complet)
    lon = lon_vals * 2 * math.pi
    # Latitude : -PI/2 à PI/2 (pôle sud à pôle nord)
    lat = (lat_vals - 0.5) * math.pi
    
    # Formules sphériques (coordonnées cartésiennes unitaires)
    nx = np.cos(lat) * np.cos(lon)
    ny = np.cos(lat) * np.sin(lon)
    nz = np.sin(lat)
    
    return nx, ny, nz