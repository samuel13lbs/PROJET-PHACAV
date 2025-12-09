
PLAN DE TEST – PROJET PHACAV
Binôme : Koami Jonathan Aziagbegnon & Andy
Période : du 10 au 13 juin 2025
Contexte : Simulation procédurale de planètes exoplanétaires

1. Objectif du plan de test



Ce document présente l’ensemble des tests conçus pour valider la robustesse, la fiabilité et la conformité fonctionnelle du projet PHACAV. Il couvre les tests unitaires, les tests d’intégration, les vérifications visuelles ainsi que l’automatisation via l’outil d’intégration continue GitLab CI.

2. Stratégie de test



- Méthodologie : développement dirigé par les tests (TDD)
- Environnement : Python 3.13, gestion de projet avec Poetry, Windows
- Outils : pytest, unittest.mock, matplotlib, numpy, GitLab CI
- Objectif de couverture : au moins 80 % de couverture de code sur les modules critiques

3. Tests par module



Module 1 – Récupération des données (responsable : Andy)
Objectif : récupération des données TRAPPIST-1e/f/g depuis l’API NASA
Tests :

- Simulation (mock) d’une réponse JSON avec tous les champs requis
- Vérification de la sauvegarde au format JSON
- Test de robustesse en cas d’échec réseau ou réponse partielle

Module 2 – Génération d’altitude (responsable : Jonathan)
Objectif : générer une heightmap 512x1024 avec bruit procédural
Tests :

- Vérification des dimensions de la matrice
- Validation des valeurs dans l’intervalle \[0.0 ; 1.0]
- Continuité horizontale sur l’image (périodicité Mercator)

Module 3 – Calcul de température (responsable : Andy)
Objectif : calculer la température globale et zonale de la planète
Tests :

- Application correcte de la formule physique (Stefan-Boltzmann)
- Modulation en fonction de la latitude
- Vérification manuelle du gradient de température sur l’image

Module 4 – Hydrosphère (responsable : Jonathan)
Objectif : identifier les zones immergées à partir de l’altitude
Tests :

- Détermination correcte de la médiane d’altitude
- Génération d’une image binaire différenciant terre et mer
- Vérification de la cohérence visuelle

Module 5 – Simulation atmosphérique (responsable : Jonathan)
Objectif : modéliser un champ vectoriel des vents
Tests :

- Répartition correcte des bandes latitudinales
- Génération d’un champ vectoriel encodé en RGB
- Validation manuelle de la direction et intensité des flux

Module 6 – Détermination des biomes (responsable : Andy)
Objectif : classifier chaque zone selon température et humidité
Tests :

- Croisement correct des cartes température et humidité
- Attribution des biomes basée sur le diagramme de Whittaker
- Test visuel de la diversité et lisibilité des zones

Module 7 – Visualisation finale (responsable : binôme)
Objectif : assembler et afficher la planète complète
Tests :

- Vérification de l’intégration des différentes couches (altitude, mer, température, biomes)
- Export d’un rendu final (PNG ou interactif)
- Validation de la lisibilité générale

4. Tests d’intégration continue



Les tests sont automatiquement lancés à chaque commit via GitLab CI.
La configuration dans .gitlab-ci.yml permet :

- L’installation automatique des dépendances via Poetry
- L’exécution de tous les tests unitaires avec pytest
- Le blocage du pipeline en cas d’échec
- La génération d’un rapport de couverture
- La vérification du score du linter

5. Organisation des fichiers de test



Le dossier tests/ contient :

- test\_api.py
- test\_surface.py
- test\_temperature.py
- test\_hydro.py
- test\_wind.py
- test\_biome.py
- test\_render.py

Chaque fichier est lié à un module et contient :

- Des assertions sur les sorties
- Des tests sur des mocks ou des données synthétiques
- Des tests de robustesse (valeurs limites, types inattendus)

6. Répartition des responsabilités



Jonathan :

- test\_surface.py
- test\_hydro.py
- test\_wind.py
- test\_render.py (couche d’assemblage finale)

Andy :

- test\_api.py
- test\_temperature.py
- test\_biome.py

Binôme :

- test\_render.py (vue générale)
- .gitlab-ci.yml
- README.md (documentation et commande de test)

7. Exécution



Local :
poetry install
pytest

CI/CD :
Configurer .gitlab-ci.yml avec :

- poetry install
- pytest

8. Conclusion



Le plan de test PHACAV s’inscrit dans une logique de qualité logicielle rigoureuse. Il vise à garantir que chaque module, traité de manière modulaire et testable, contribue à la cohérence et au réalisme de la simulation finale. L’automatisation des tests via GitLab CI sécurise le développement collaboratif entre Andy et Jonathan.




