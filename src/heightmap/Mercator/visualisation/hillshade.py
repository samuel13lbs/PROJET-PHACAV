import numpy as np

def hillshade(elevation, azimuth=315, altitude=45):
    x, y = np.gradient(elevation)

    slope = np.pi / 2.0 - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)

    azimuth = np.deg2rad(azimuth)
    altitude = np.deg2rad(altitude)

    shaded = (
        np.sin(altitude) * np.sin(slope) +
        np.cos(altitude) * np.cos(slope) *
        np.cos(azimuth - aspect)
    )

    return (shaded + 1) / 2