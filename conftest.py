import os
import sys
from pathlib import Path

# Obtenir le chemin absolu du projet
project_root = Path(__file__).parent.absolute()

# Ajouter le dossier src au PYTHONPATH
src_path = str(project_root / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Afficher le PYTHONPATH pour le débogage
print(f"PYTHONPATH: {sys.path}") 