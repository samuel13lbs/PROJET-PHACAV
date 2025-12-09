
classDiagram

class APIClient {
    +fetch_exoplanet_data(name: str) : dict
}

class HeightmapGenerator {
    +generate(width: int, height: int, scale: float) : ndarray
}

class HydrosphereAnalyzer {
    +analyze(heightmap: ndarray) : ndarray
}

class TemperatureMap {
    +compute(planet_data: dict) : ndarray
}

class WindSimulator {
    +simulate(heightmap: ndarray) : ndarray
}

class BiomeClassifier {
    +classify(temperature: ndarray, humidity: ndarray) : ndarray
}

class Renderer {
    +render2D(layers: list) : void
    +render3D() : void
}

class PlanetBuilder {
    +build_planet(name: str) : Planet
}

class ConfigSingleton {
    +get_instance() : ConfigSingleton
    +get(key: str) : any
}

class Planet {
    +name: str
    +mass: float
    +radius: float
    +star_data: dict
    +altitude_map: ndarray
    +temperature_map: ndarray
    +humidity_map: ndarray
    +biome_map: ndarray
}

<<singleton>> ConfigSingleton

PlanetBuilder --> APIClient
PlanetBuilder --> HeightmapGenerator
PlanetBuilder --> TemperatureMap
PlanetBuilder --> HydrosphereAnalyzer
PlanetBuilder --> WindSimulator
PlanetBuilder --> BiomeClassifier
PlanetBuilder --> Renderer
PlanetBuilder --> ConfigSingleton
PlanetBuilder --> Planet


https://www.mermaidchart.com/app/projects/43ed4eb6-38e7-4748-b977-c77d6cc38fbf/diagrams/7bf8b2c7-a9cf-428c-b30d-b09b13d92827/version/v0.1/edit
