import os
import sys
import json
import numpy as np

# Assurer que l'on peut importer les modules locaux
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_retriever import NASAExoplanetAPI, save_data_to_file
# Import avec le nom exact du fichier qui contient des accents/espaces si nécessaire
# Comme le fichier s'appelle "Calcul_température.py", on l'importe ainsi :
import Calcul_température as clim

def main():
    print("--- Démarrage du Test Calcul Température ---")

    # 1. Récupération des données
    print("1. Récupération des données API...")
    api = NASAExoplanetAPI()
    df = api.get_trappist1_planets_data()
    
    if df is None:
        print("❌ Erreur: Impossible de récupérer les données.")
        return

    # Sauvegarde locale pour inspection
    # On force le dossier data local au script
    os.makedirs("data", exist_ok=True)
    # Patch rapide pour que save_data_to_file utilise le bon dossier data relatif
    # (ou on suppose qu'il écrit dans ./data par défaut si executé depuis le dossier)
    save_data_to_file(df, "trappist1_planets.json", "json")

    # 2. Extraction des paramètres pour TRAPPIST-1 e
    print("2. Extraction des données pour TRAPPIST-1 e...")
    # Conversion du DF en dictionnaires
    records = df.to_dict(orient="records")
    planet_data = next((p for p in records if p["pl_name"] == "TRAPPIST-1 e"), None)

    if not planet_data:
        print("❌ Erreur: TRAPPIST-1 e non trouvée dans les données.")
        return

    teff = planet_data["st_teff"]
    rad = planet_data["st_rad"]
    
    print(f"   - Température étoile : {teff} K")
    print(f"   - Rayon étoile : {rad} rayons solaires")

    # 3. Calculs
    print("3. Exécution des calculs thermiques...")
    
    # Calcul luminosité
    luminosite = clim.calculer_luminosite(teff, rad)
    print(f"   - Luminosité calculée : {luminosite:.2e} W")

    # Calcul température moyenne
    # Note: On utilise la distance par défaut définie dans le module si non spécifiée,
    # ou on pourrait la récupérer de l'API (sy_dist est la distance du SYSTEME, pas de la planète à l'étoile)
    # Le code original utilise une constante DIST_ETOILE hardcodée pour Trappist-1, on garde ça pour l'instant.
    temp_moyenne = clim.calculer_temp_moyenne(luminosite)
    print(f"   - Température moyenne de surface : {temp_moyenne:.2f} K")

    # Création du profil zonal
    profil = clim.creer_profil_zones(temp_moyenne)
    
    # 4. Génération des visuels
    print("4. Génération des graphiques et textures...")
    # Latitude pour le graphique
    lats = np.linspace(-90, 90, clim.NB_POINTS)
    
    # Tracer graphique
    # Attention: le module écrit dans "data/...", il faut s'assurer que ça pointe au bon endroit
    clim.tracer_graphique(lats, profil)
    
    # Générer image
    clim.generer_image_thermique(profil)

    print("--- Test Terminé avec Succès ---")
    print("Vérifiez le dossier 'data/' pour les résultats.")

if __name__ == "__main__":
    # Changement du dossier de travail pour que les fichiers 'data/' s'écrivent au bon endroit
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
