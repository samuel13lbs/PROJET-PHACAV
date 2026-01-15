"""
MODULE ATMOSPHÈRE & VENTS
------------------------
Rôle :
- Entrées  : altitude, température, précipitations, latitude, longitude
- Sorties  : cartes de vents (u, v, vitesse, direction)
        cartes atmosphériques (température ajustée, humidité, pression, nuages)

Hypothèses physiques (simplifiées mais cohérentes) :
- Effet de Coriolis
- Gradient thermique (vent géostrophique)
- Effet du relief
- Cellules de Hadley / Ferrel / Polaire
- Cyclones statiques (non temporels)

Aucune dépendance temporelle : module purement déterministe
(sauf composante aléatoire contrôlable pour les cyclones).
"""

import numpy as np
from typing import Dict
from scipy.ndimage import gaussian_filter

# OUTILS GÉOGRAPHIQUES
def generer_grilles(latitudes: int, longitudes: int):
    """Génère les grilles latitude / longitude"""
    lats = np.linspace(-90, 90, latitudes)
    lons = np.linspace(-180, 180, longitudes)
    lat_grid, lon_grid = np.meshgrid(lats, lons, indexing="ij")
    return lat_grid, lon_grid

# CELLULES ATMOSPHÉRIQUES
def cellules_atmospheriques(lat_grid):
    hadley = np.exp(-(lat_grid / 25)**2)
    ferrel = np.exp(-((np.abs(lat_grid) - 45) / 15)**2)
    polaire = np.exp(-((np.abs(lat_grid) - 75) / 10)**2)
    
    u = (-6 * hadley + 12 * ferrel * np.sign(lat_grid) + 15 * polaire * np.sign(lat_grid))
    v = (-3 * hadley * np.sign(lat_grid) + 2 * polaire * np.sign(lat_grid))
    
    return u, v

# CYCLONES STATIQUES
def champ_cyclonique(lat_grid, lon_grid, temperature, nb=5, seed=None):
    if seed is not None:
        np.random.seed(seed)

    u_total = np.zeros_like(lat_grid)
    v_total = np.zeros_like(lat_grid)
    for _ in range(nb):
        clat = np.random.uniform(-30, 30)
        clon = np.random.uniform(-180, 180)
        
        dy = (lat_grid - clat) * 111
        dx = (lon_grid - clon) * 111 * np.cos(np.radians(clat))
        r = np.sqrt(dx**2 + dy**2) + 1e-6

        sens = np.sign(clat) if clat != 0 else 1
        intensite = np.random.uniform(10, 25)
        rayon = np.random.uniform(250, 500)

        facteur_temp = np.clip((temperature + 10) / 40, 0, 1)
        u = -sens * intensite * dy / r * np.exp(-(r / rayon)**2)
        v =  sens * intensite * dx / r * np.exp(-(r / rayon)**2)

        u_total += u * facteur_temp
        v_total += v * facteur_temp

    return u_total, v_total

# GÉNÉRATION DES VENTS
def generer_vents(
    altitude: np.ndarray,
    temperature: np.ndarray,
    lat_grid: np.ndarray,
    lon_grid: np.ndarray,
    nb_cyclones: int = 5
):
    # -------- Coriolis --------
    omega = 7.2921e-5
    f = 2 * omega * np.sin(np.radians(lat_grid)) + 1e-10

    # -------- Gradient thermique --------
    dTdy, dTdx = np.gradient(temperature)
    u_geo = -0.3 * dTdy / f
    v_geo =  0.3 * dTdx / f

    # -------- Relief --------
    dHdy, dHdx = np.gradient(altitude)
    u_relief = -0.001 * dHdx
    v_relief = -0.001 * dHdy

    # -------- Cellules globales --------
    u_cell, v_cell = cellules_atmospheriques(lat_grid)

    # -------- Cyclones --------
    u_cyc, v_cyc = champ_cyclonique(
        lat_grid, lon_grid, temperature, nb=nb_cyclones
    )

    # -------- Combinaison --------
    u = u_geo + u_relief + u_cell + u_cyc
    v = v_geo + v_relief + v_cell + v_cyc

    # -------- Lissage & limites --------
    u = gaussian_filter(u, sigma=1.5)
    v = gaussian_filter(v, sigma=1.5)

    u = np.clip(u, -40, 40)
    v = np.clip(v, -40, 40)
    vitesse = np.sqrt(u**2 + v**2)
    direction = (np.degrees(np.arctan2(v, u)) + 360) % 360

    return u, v, vitesse, direction

# ATMOSPHÈRE
def generer_atmosphere(
    altitude: np.ndarray,
    temperature: np.ndarray,
    precipitation: np.ndarray,
    vitesse_vent: np.ndarray
):
    temperature_adj = temperature - 0.0065 * altitude
    humidite = np.clip(precipitation / 3000, 0, 1)
    pression = 1013 - 0.12 * altitude - 0.8 * vitesse_vent
    nuages = np.clip(humidite * vitesse_vent / 20, 0, 1)

    return temperature_adj, humidite, pression, nuages

# INTERFACE
def calculer_vents_et_atmosphere(
    altitude: np.ndarray,
    temperature: np.ndarray,
    precipitation: np.ndarray,
    lat_grid: np.ndarray,
    lon_grid: np.ndarray,
    nb_cyclones: int = 5
) -> Dict:

    u, v, vitesse, direction = generer_vents(
        altitude,
        temperature,
        lat_grid,
        lon_grid,
        nb_cyclones
    )

    temp_adj, humidite, pression, nuages = generer_atmosphere(
        altitude,
        temperature,
        precipitation,
        vitesse
    )

    return {
        "vents": {
            "u": u,
            "v": v,
            "vitesse": vitesse,
            "direction": direction
        },
        "atmosphere": {
            "temperature": temp_adj,
            "humidite": humidite,
            "pression": pression,
            "nuages": nuages
        }
    }
