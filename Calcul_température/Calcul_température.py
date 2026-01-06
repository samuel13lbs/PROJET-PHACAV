import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Constantes

REFLECTIVITE = 0.306
DIST_ETOILE = 0.0293 * 1.496e11 
HAUTEUR_IMG = 512
LARGEUR_IMG = 1024
NB_POINTS = 512
CONST_STEFAN = 5.67e-8
RAYON_SOLEIL = 6.96e8


def calculer_luminosite(temp_etoile: float, rayon_relatif: float) -> float:

    # Calcule la luminosité de l'étoile.

    rayon_metres = rayon_relatif * RAYON_SOLEIL
    return 4 * np.pi * rayon_metres**2 * CONST_STEFAN * temp_etoile**4





def calculer_temp_moyenne(
    luminosite: float,
    reflectivite: float = REFLECTIVITE,
    distance: float = DIST_ETOILE
) -> float:

    # Calcule la température moyenne de la plaanète.
    haut = luminosite * (1 - reflectivite)
    bas = 16 * np.pi * CONST_STEFAN * distance**2
    return (haut / bas) ** 0.25







def creer_profil_zones(temp_moyenne: float, nb_pts: int = NB_POINTS) -> np.ndarray:
    
    # Crée un profil de température selon les zones de latitude.
    # Maximum à l'équateur, minimum aux pôles.
    
    lats = np.linspace(-90, 90, nb_pts)
    return temp_moyenne * (np.cos(np.radians(lats))) ** 2



def generer_image_thermique(
    temperatures: np.ndarray,
    largeur: int = LARGEUR_IMG,
    fichier_sortie: str = "data/texture_thermique.png"
):
    # Génère une image thermique 2D
    normalise = (temperatures - temperatures.min()) / (temperatures.max() - temperatures.min())
    palette = plt.get_cmap("inferno")
    couleurs = (palette(normalise)[:, :3] * 255).astype(np.uint8)
    image = np.repeat(couleurs[np.newaxis, :, :], largeur, axis=0).transpose(1, 0, 2)
    Image.fromarray(image).save(fichier_sortie)
    print(f"✅ {fichier_sortie} créé")





def tracer_graphique(latitudes: np.ndarray, temperatures: np.ndarray):

    # Trace le graphique température vs latitude.
    plt.figure(figsize=(8, 4))
    plt.plot(latitudes, temperatures, label="Profil de température")
    plt.xlabel("Latitude (°)")
    plt.ylabel("Température (K)")
    plt.title("Distribution de température par latitude")
    plt.grid(True)
    plt.legend()
    plt.savefig("data/graphique_temp.png")
    plt.close()
    print("✅ data/graphique_temp.png créé")