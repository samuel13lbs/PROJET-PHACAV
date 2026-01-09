import numpy as np

def generate_ridges(width, height):
    ridges = np.zeros((height, width))
    center = width // 2

    for y in range(height):
        for x in range(width):
            dist = abs(x - center) / width
            ridges[y][x] = max(0, 1 - dist * 6)

    return ridges