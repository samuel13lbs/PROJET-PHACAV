import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource
from visualisation.colormap import terrain_colormap

def render_altitude_map(altitude_map, title="Rendu Relief 3D Simulé"):
    """
    Rendu HD avec simulation de relief par ombrage porté.
    """
    # 1. Récupération des couleurs de colormap.py
    cmap = terrain_colormap()

    # 2. Création de la source de lumière pour l'effet 3D
    ls = LightSource(azdeg=315, altdeg=45)

    # 3. Calcul de l'ombrage (Hillshade)
    rgb = ls.shade(altitude_map, cmap=cmap, blend_mode='soft', vert_exag=0.05)

    plt.figure(figsize=(16, 8), facecolor='#050505') # Fond noir spatial
    
    plt.imshow(rgb, origin='lower', interpolation='bicubic')
    
    plt.title(title, color='white', fontsize=15, pad=20)
    plt.axis("off")
    plt.tight_layout()
    
    print("Affichage du rendu HD terminé.")
    plt.show()