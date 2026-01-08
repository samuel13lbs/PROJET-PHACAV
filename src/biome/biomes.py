import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from PIL import Image

class BiomeDeterminer:
    def __init__(self, width=512, height=1024):
        self.width = width
        self.height = height
        self.perlin = PerlinNoise(octaves=6)
        self.biomes = ['Océan', 'Désert froid', 'Toundra', 'Tundra', 'Taïga', 
                      'Forêt tempérée', 'Savane', 'Forêt tropicale', 'Désert chaud']

    def generate_altitude(self, scale=100):
        altitude = np.zeros((self.height, self.width))
        for i in range(self.height):
            lat = np.pi * (0.5 - i / self.height)
            y_scale = np.cos(lat)
            for j in range(self.width):
                x = (j / self.width) * scale * y_scale
                y = (i / self.height) * scale
                altitude[i, j] = self.perlin([x, y])
        return (altitude + 1) / 2  # [-1,1] → [0,1]

    def temperature_map(self, altitude):
        """ Températures VARIÉES pour TRAPPIST-1e"""
        temp_equator = np.random.uniform(-5, 10)
        temp_map = np.zeros((self.height, self.width))
        for i in range(self.height):
            lat = abs(np.pi * (0.5 - i / self.height))
            temp_base = temp_equator * (np.cos(lat)**1.5)
            temp_noise = self.perlin([i*0.01, np.random.rand()])*2  # ✅ Marche direct
            temp_map[i, :] = temp_base * (1 - 0.5 * altitude[i, :]) + temp_noise
        return np.clip(temp_map, -50, 25)

    def humidity_map(self, altitude):
        """ TOUTES LES MÉTHODES SONT LÀ"""
        sea_level = 0.45
        humidity = np.zeros_like(altitude)
        humidity[altitude < sea_level] = 1.0
        land = altitude >= sea_level
        humidity[land] = 0.3 * np.exp(-3 * (altitude[land] - sea_level))
        return np.clip(humidity, 0, 1)

    def determine_biomes(self, temp_map, humidity_map, altitude):
        """ Whittaker RÉEL"""
        biome_map = np.zeros((self.height, self.width), dtype=int)
        sea_level = 0.45
        
        for i in range(self.height):
            for j in range(self.width):
                if altitude[i, j] < sea_level:
                    biome_map[i, j] = 0
                    continue
                    
                temp = temp_map[i, j]
                precip = humidity_map[i, j] * 1000  # mm/an
                
                if precip < 50:  # Déserts
                    biome_map[i, j] = 8 if temp > 10 else 1
                elif precip < 300:  # Steppes
                    biome_map[i, j] = 5 if temp > 0 else 2
                elif precip < 800:  # Forêts
                    biome_map[i, j] = 4 if temp < 10 else 7
                else:  # Très humide
                    biome_map[i, j] = 7 if temp > 5 else 3
        
        return biome_map

    def visualize(self, biome_map, altitude, temp_map, hum_map):
        colors = np.array([
            [0, 51, 255], [200, 200, 200], [240, 240, 240], [170, 220, 170],
            [34, 102, 34], [68, 136, 68], [220, 170, 68], [0, 136, 0], [255, 221, 136]
        ], dtype=np.uint8)
        
        colored = colors[biome_map % len(colors)]
        Image.fromarray(colored).save('biomes.png')
        
        fig, axs = plt.subplots(2, 2, figsize=(15, 25))
        axs[0,0].imshow(altitude, cmap='terrain')
        axs[0,0].set_title('Altitude')
        axs[0,1].imshow(temp_map, cmap='coolwarm', vmin=-50, vmax=25)
        axs[0,1].set_title('Température')
        axs[1,0].imshow(hum_map, cmap='Blues')
        axs[1,0].set_title('Humidité')
        axs[1,1].imshow(colored)
        axs[1,1].set_title('Biomes')
        for ax in axs.flat: ax.axis('off')
        plt.tight_layout()
        plt.savefig('biomes_full.png', dpi=150, bbox_inches='tight')
        plt.show()

#  EXÉCUTION
determiner = BiomeDeterminer()
altitude = determiner.generate_altitude()
temp_map = determiner.temperature_map(altitude)
hum_map = determiner.humidity_map(altitude)
biomes = determiner.determine_biomes(temp_map, hum_map, altitude)
determiner.visualize(biomes, altitude, temp_map, hum_map)
print(" TERMINÉ!")
