# PHACAV - Planète Habitable Au Climat Analogue Virtuel

> Projet Python de simulation procédurale de planètes, basé sur des données réelles d'exoplanètes issues de la NASA.  
> Réalisé en binôme à l'ESIEA – Juin 2025.

---

## Objectifs

- Récupérer les données exoplanétaires depuis l'API NASA
- Générer de la topographie procédurale (relief)
- Simuler le climat : température, humidité, océans
- Classer les zones en biomes (toundra, désert, forêt…)
- Visualiser le tout en 2D (cartes) et 3D (globe interactif)

---

## Technologies

- **Langage** : Python 3.8+  
- **Librairies clés** :  
  - `numpy`: Calculs matriciels et manipulation de données
  - `noise`: Génération de bruit de Perlin pour les heightmaps
  - `matplotlib`: Visualisation 2D (<3.10)
  - `requests`: Communication avec l'API NASA (>=2.32.4,<3.0.0)
  - `pytest`: Tests unitaires et d'intégration

---

## Architecture du Projet

Le projet suit une architecture modulaire où chaque composant est responsable d'un aspect spécifique de la simulation planétaire :

### 1. API NASA (`src/api/`)
- Récupération des données d'exoplanètes via l'API NASA Exoplanet Archive
- Stockage des données dans `data/exoplanets.json`
- Formatage des données pour l'utilisation interne

### 2. Heightmap (`src/heightmap/`)
- Génération de cartes d'altitude via bruit de Perlin
- Paramètres configurables :
  - `scale`: Échelle du bruit (défaut: 100.0)
  - `octaves`: Nombre de couches de bruit (défaut: 6)
  - `persistence`: Amortissement de l'amplitude (défaut: 0.5)
  - `lacunarity`: Augmentation de la fréquence (défaut: 2.0)
- Continuité aux bords garantie pour le rendu sphérique

### 3. Atmosphère (`src/atmosphere/`)
- Simulation des conditions atmosphériques
- Génération de bruit multi-échelle
- Prise en compte de la latitude pour la distribution atmosphérique

### 4. Hydrosphère (`src/hydro/`)
- Simulation des corps d'eau basée sur la heightmap
- Paramètres :
  - `sea_level`: Niveau de la mer (défaut: 0.5)
  - Prise en compte de l'évaporation et des précipitations
  - Simulation des courants marins

### 5. Climat (`src/climate/`)
- Modélisation des conditions climatiques
- Facteurs considérés :
  - Latitude
  - Altitude
  - Proximité des océans
  - Circulation atmosphérique

### 6. Biomes (`src/biome/`)
- Classification des zones en biomes
- Basée sur :
  - Température
  - Précipitations
  - Altitude
  - Type de sol

### 7. Rendu (`src/render/`)
- Visualisation 2D avec matplotlib
- Visualisation 3D avec pyvista
- Support du backend non-interactif pour les tests
- Export d'images en haute résolution

---

## Installation

1. **Prérequis**
   ```bash
   # Python 3.8 ou supérieur
   python --version
   ```

2. **Cloner le Projet**
   ```bash
   git clone https://gitlab.esiea.fr/aziagbenon/phacav-andy-jonathan.git
   cd phacav-andy-jonathan
   ```

3. **Installation des Dépendances**
   ```bash
   pip install -r requirements.txt
   ```

---

## Utilisation

### Génération d'une Planète

```python
from src.heightmap.heightmap_generator import HeightmapGenerator
from src.atmosphere.atmosphere import AtmosphereSimulator
from src.hydro.hydrosphere import HydrosphereSimulator
from src.render.renderer import Renderer

# 1. Génération de la heightmap
heightmap_gen = HeightmapGenerator(width=1024, height=512)
heightmap = heightmap_gen.generate()

 ```bash
 python visualize_planet_3d.py

---

## Tests

### Tests Unitaires
```bash
# Exécuter tous les tests
pytest

# Tests spécifiques
pytest test/test_heightmap.py
pytest test/test_atmosphere.py
pytest test/test_hydro.py
```

### Tests d'Intégration
```bash
pytest test/test_integration.py
```

### Structure des Tests

- `test_heightmap.py`: Tests de génération de heightmap
- `test_atmosphere.py`: Tests de simulation atmosphérique
- `test_hydro.py`: Tests de simulation hydrologique
- `test_render.py`: Tests de rendu
- `test_integration.py`: Tests d'intégration complète

 Andy ESSOMBA

## Auteurs

- Andy Jonathan
- Jazia Aziagbenon


