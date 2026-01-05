from pathlib import Path
import requests
import pandas as pd
import json
from dataclasses import dataclass


# ======================================================
# 1 Modèle de données
# ======================================================
class Exoplanet:
    def __init__(self, name, star, radius, mass, temp, distance):
        self.name = name
        self.star = star
        self.radius = radius
        self.mass = mass
        self.temp = temp
        self.distance = distance

    def to_dict(self):
        return {
            "pl_name": self.name,
            "hostname": self.star,
            "pl_rade": self.radius,
            "pl_masse": self.mass,
            "st_teff": self.temp,
            "sy_dist": self.distance
        }



# ======================================================
# 2 Client API NASA
# ======================================================
class NasaExoplanetAPI:
    BASE_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

    def fetch_trappist_g(self) -> pd.DataFrame:
        """
        Récupère les entrées TRAPPIST-1 g depuis la NASA
        """
        query = """
        SELECT pl_name, hostname, pl_rade, pl_masse, st_teff, sy_dist
        FROM ps
        WHERE pl_name = 'TRAPPIST-1 g'
        """

        params = {
            "query": query,
            "format": "json"
        }

        response = requests.get(self.BASE_URL, params=params, timeout=15)

        if response.status_code != 200:
            raise RuntimeError(f"NASA API error: {response.status_code}")

        return pd.DataFrame(response.json())


# ======================================================
# 3 Traitement des données
# ======================================================
class ExoplanetService:

    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        - Supprime les doublons
        - Garde la ligne la plus complète
        """
        df = df.dropna(how="all")

        # Trier pour garder les valeurs les plus riches
        df = df.sort_values(
            by=["pl_masse", "pl_rade"],
            ascending=False
        )

        # Supprimer doublons
        df = df.drop_duplicates(subset=["pl_name"], keep="first")

        return df

    @staticmethod
    def to_exoplanet(df: pd.DataFrame) -> Exoplanet:
        """
        Convertit le DataFrame final en Exoplanet
        """
        row = df.iloc[0]
        return Exoplanet(
            name=row["pl_name"],
            star=row["hostname"],
            radius=row["pl_rade"],
            mass=row["pl_masse"],
            temp=row["st_teff"],
            distance=row["sy_dist"]
        )


# ======================================================
# 4 Exporteurs
# ======================================================
class Exporter:

    @staticmethod
    def to_json(planet: Exoplanet, filename="trappist_1_g.json"):
        data_dir = Path("data")
        # Dossier data/
        data_dir.mkdir(exist_ok=True)

        file_path = data_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(planet.to_dict(), f, indent=2, ensure_ascii=False)

        print(f"✔ JSON créé : {file_path}")

    @staticmethod
    def to_csv(df: pd.DataFrame, filename="trappist_1_g.csv"):
        # Dossier data/
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        file_path = data_dir / filename

        df.to_csv(file_path, index=False)
        print(f"✔ CSV créé : {file_path}")


# ======================================================
# 5 Programme principal
# ======================================================
