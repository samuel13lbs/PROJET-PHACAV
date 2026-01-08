import numpy as np


class Hydrosphere:

    def __init__(
        self,
        niveau_mer: float = 0.0,
        seuil_côte: float = 0.05
    ):
        self.niveau_mer = niveau_mer
        self.seuil_côte = seuil_côte

    def compute(self, altitude_map: np.ndarray) -> np.ndarray:

        if altitude_map.ndim != 2:
            raise ValueError("altitude_map doit être une matrice 2D")

        water_map = np.zeros_like(altitude_map, dtype=np.uint8)

        ocean_mask = altitude_map < self.niveau_mer

        coast_mask = np.abs(altitude_map - self.niveau_mer) <= self.seuil_côte

        land_mask = altitude_map > self.niveau_mer + self.seuil_côte

        water_map[ocean_mask] = 0
        water_map[coast_mask] = 1
        water_map[land_mask] = 2

        return water_map
