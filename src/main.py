from api.exoplanet_fetcher import ExoplanetService, Exporter, NasaExoplanetAPI


def main():
    api = NasaExoplanetAPI()
    
    # Récupération
    df = api.fetch_trappist_g()

    # Nettoyage
    df_clean = ExoplanetService.clean_dataframe(df)

    # Conversion
    planet = ExoplanetService.to_exoplanet(df_clean)
    print(f"\nDonnées de l’exoplanète : {planet.to_dict()}")
    # Export
    Exporter.to_json(planet)
    Exporter.to_csv(df_clean)

    print("\n Données TRAPPIST-1 g prêtes à l’utilisation.")


if __name__ == "__main__":
    main()
