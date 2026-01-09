import matplotlib.pyplot as plt
from config.planet_config import PLANET_CONFIG
from terrain.altitude import generate_altitude_map

altitude_map = generate_altitude_map(PLANET_CONFIG)

plt.figure(figsize=(12, 6))
plt.imshow(altitude_map, cmap="gray")
plt.axis("off")
plt.title("Carte d'altitude planétaire")
plt.show()