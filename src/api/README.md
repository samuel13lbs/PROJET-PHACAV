# Module API - Récupération de Données d'Exoplanètes

Ce module permet de récupérer les données d'exoplanètes depuis la **NASA Exoplanet Archive** via le service TAP (Table Access Protocol).

## 🌟 Fonctionnalités

- ✅ Récupération de données pour une ou plusieurs exoplanètes
- ✅ Données complètes sur les planètes ET leurs étoiles hôtes
- ✅ Filtrage des candidats en zone habitable
- ✅ Export en JSON et CSV
- ✅ Gestion des erreurs et validation des données
- ✅ Interface simple et intuitive

## 📊 Données Récupérées

### Données Planétaires
- Nom de la planète
- Distance du système (parsecs)
- Rayon (rayons terrestres)
- Masse (masses terrestres)
- Densité (g/cm³)
- Température d'équilibre (K)
- Flux stellaire
- Période orbitale (jours)
- Demi-grand axe (UA)
- Année et méthode de découverte

### Données Stellaires
- Nom de l'étoile hôte
- Température effective (K)
- Rayon stellaire (rayons solaires)
- Masse stellaire (masses solaires)
- Luminosité (luminosités solaires)
- Type spectral
- Âge (Gyr)
- Métallicité [Fe/H]
- Nombre d'étoiles et de planètes dans le système

## 🚀 Utilisation

### Installation des dépendances

Les dépendances nécessaires sont déjà dans `requirements.txt`:
- `requests` >= 2.26.0
- `pandas` >= 2.3.0

### Exemple 1: Récupérer une planète spécifique

```python
from src.api.exoplanet_fetcher import ExoplanetFetcher

# Créer une instance
fetcher = ExoplanetFetcher(output_dir="data")

# Récupérer Kepler-186 f
planet_data = fetcher.fetch_exoplanet_by_name("Kepler-186 f")

# Afficher le résumé
print(fetcher.get_planet_summary(planet_data))

# Sauvegarder en JSON
fetcher.save_to_json(planet_data, "kepler_186_f")
```

### Exemple 2: Récupérer plusieurs planètes

```python
planet_names = [
    "Kepler-186 f",
    "Proxima Cen b",
    "TRAPPIST-1 e",
    "K2-18 b"
]

planets_data = fetcher.fetch_multiple_exoplanets(planet_names)
fetcher.save_to_json(planets_data, "selected_exoplanets")
```

### Exemple 3: Candidats de la zone habitable

```python
# Récupérer jusqu'à 50 candidats
habitable_df = fetcher.fetch_habitable_zone_candidates(limit=50)

# Sauvegarder en JSON et CSV
fetcher.save_to_json(habitable_df, "habitable_candidates")
fetcher.save_to_csv(habitable_df, "habitable_candidates")
```

### Exemple 4: Toutes les planètes confirmées

```python
# Récupérer toutes les planètes (peut être long!)
all_planets = fetcher.fetch_confirmed_planets()

# Ou limiter le nombre
sample = fetcher.fetch_confirmed_planets(limit=100)
```

## 📝 Script d'Exemple Complet

Un script d'exemple complet est disponible dans `examples/fetch_exoplanet_data.py`:

```bash
python examples/fetch_exoplanet_data.py
```

Ce script démontre toutes les fonctionnalités du module.

## 🔍 Critères de Zone Habitable

Le module utilise les critères suivants pour identifier les candidats potentiellement habitables:

- **Rayon**: 0.5 - 2.0 rayons terrestres
- **Température d'équilibre**: 200 - 350 K
- **Flux stellaire**: 0.25 - 4.0 flux terrestres

Ces critères sont approximatifs et basés sur notre compréhension actuelle de l'habitabilité.

## 📁 Format de Sortie

### JSON (planète unique)
```json
{
  "planet": {
    "pl_name": "Kepler-186 f",
    "hostname": "Kepler-186",
    "sy_dist": 151.0,
    "pl_rade": 1.17,
    "pl_masse": null,
    "pl_eqt": 188.0,
    ...
  },
  "host_star": {
    "hostname": "Kepler-186",
    "st_teff": 3755.0,
    "st_rad": 0.52,
    "st_mass": 0.54,
    ...
  }
}
```

### JSON (plusieurs planètes)
```json
[
  {
    "planet": {...},
    "host_star": {...}
  },
  {
    "planet": {...},
    "host_star": {...}
  }
]
```

### CSV
Format tabulaire avec toutes les colonnes disponibles.

## 🛠️ API Reference

### Classe `ExoplanetFetcher`

#### `__init__(output_dir="data")`
Initialise le fetcher avec un répertoire de sortie.

#### `fetch_exoplanet_by_name(planet_name: str) -> Dict`
Récupère les données d'une planète spécifique.

**Paramètres:**
- `planet_name`: Nom de la planète (ex: "Kepler-186 f")

**Retourne:** Dictionnaire avec clés `planet` et `host_star`

#### `fetch_multiple_exoplanets(planet_names: List[str]) -> List[Dict]`
Récupère les données de plusieurs planètes.

**Paramètres:**
- `planet_names`: Liste des noms de planètes

**Retourne:** Liste de dictionnaires

#### `fetch_habitable_zone_candidates(limit: int = 50) -> pd.DataFrame`
Récupère les candidats potentiellement habitables.

**Paramètres:**
- `limit`: Nombre maximum de résultats

**Retourne:** DataFrame pandas

#### `fetch_confirmed_planets(limit: Optional[int] = None) -> pd.DataFrame`
Récupère toutes les planètes confirmées.

**Paramètres:**
- `limit`: Nombre maximum de résultats (None = tous)

**Retourne:** DataFrame pandas

#### `save_to_json(data, filename: str) -> Path`
Sauvegarde les données au format JSON.

#### `save_to_csv(data: pd.DataFrame, filename: str) -> Path`
Sauvegarde les données au format CSV.

#### `get_planet_summary(planet_data: Dict) -> str`
Génère un résumé lisible des données.

## 🌐 Source des Données

Les données proviennent de la **NASA Exoplanet Archive**:
- URL: https://exoplanetarchive.ipac.caltech.edu/
- Service: TAP (Table Access Protocol)
- Table: `ps` (Planetary Systems)

## ⚠️ Notes Importantes

1. **Connexion Internet**: Une connexion active est requise
2. **Timeout**: Les requêtes ont un timeout de 30 secondes
3. **Données manquantes**: Certaines planètes peuvent avoir des valeurs `null` pour certains paramètres
4. **Noms exacts**: Les noms de planètes doivent être exacts (sensible à la casse)

## 🔗 Ressources

- [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)
- [Documentation TAP](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html)
- [Liste des exoplanètes](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS)
