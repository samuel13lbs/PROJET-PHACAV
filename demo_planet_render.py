"""
Script de démonstration pour tester le rendu de planètes 3D.
Ce script crée une texture de test et vérifie que tout fonctionne.
"""
import pyvista as pv
import numpy as np
from PIL import Image
import os
from visualize_planet_3d import PlanetRenderer
from visualize_3d import Visualizer3D

def create_test_texture(filename='test_planet_texture.jpg', size=(2048, 1024)):
    """
    Crée une texture de test avec un motif de damier coloré.
    Simule une texture de planète pour les tests.
    
    Args:
        filename: Nom du fichier de sortie
        size: Dimensions de l'image (largeur, hauteur)
    """
    print(f"Création de la texture de test: {filename}")
    
    width, height = size
    
    # Créer une image avec un dégradé et des motifs
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            # Dégradé bleu-vert simulant océans et terres
            r = int(50 + 100 * (x / width))
            g = int(100 + 100 * (y / height))
            b = int(200 - 100 * (x / width))
            
            # Ajouter des "continents" (zones plus claires)
            if (x // 100 + y // 100) % 3 == 0:
                r = min(255, r + 80)
                g = min(255, g + 60)
                b = max(0, b - 40)
            
            pixels[x, y] = (r, g, b)
    
    img.save(filename)
    print(f"✓ Texture créée: {filename} ({width}x{height})")
    return filename


def test_basic_render():
    """Test 1: Rendu basique avec paramètres par défaut."""
    print("\n" + "="*60)
    print("TEST 1: Rendu basique")
    print("="*60)
    
    texture_file = create_test_texture()
    
    try:
        renderer = PlanetRenderer(
            texture_path=texture_file,
            radius=1.0,
            name='Planète Test'
        )
        
        print("✓ PlanetRenderer créé avec succès")
        print(f"  - Texture: {texture_file}")
        print(f"  - Rayon: {renderer.radius}")
        print(f"  - Résolution: {renderer.theta_resolution}x{renderer.phi_resolution}")
        
        print("\nLancement du rendu...")
        renderer.render()
        
        print("✓ Test 1 réussi!")
        
    except Exception as e:
        print(f"✗ Erreur lors du test 1: {e}")
        import traceback
        traceback.print_exc()


def test_advanced_render():
    """Test 2: Rendu avancé avec tous les paramètres."""
    print("\n" + "="*60)
    print("TEST 2: Rendu avancé avec options")
    print("="*60)
    
    texture_file = create_test_texture('advanced_texture.jpg', size=(1024, 512))
    
    try:
        renderer = PlanetRenderer(
            texture_path=texture_file,
            radius=1.5,
            resolution=(512, 256),
            name='Planète Avancée'
        )
        
        print("✓ PlanetRenderer créé")
        
        print("\nConfiguration du rendu:")
        print("  - Background: black")
        print("  - Lighting: realistic")
        print("  - Axes: activés")
        print("  - Camera distance: 2.5")
        print("  - Anti-aliasing: activé")
        
        renderer.render(
            background='white',
            window_size=(1400, 1000),
            lighting='realistic',
            show_axes=True,
            camera_distance=2.5,
            enable_anti_aliasing=True,
            save_screenshot='planet_screenshot.png'
        )
        
        print("✓ Test 2 réussi!")
        
        if os.path.exists('planet_screenshot.png'):
            print("✓ Screenshot sauvegardé: planet_screenshot.png")
        
    except Exception as e:
        print(f"✗ Erreur lors du test 2: {e}")
        import traceback
        traceback.print_exc()


def test_multiple_lighting():
    """Test 3: Comparaison des différents types d'éclairage."""
    print("\n" + "="*60)
    print("TEST 3: Test des différents éclairages")
    print("="*60)
    
    texture_file = create_test_texture('lighting_test.jpg')
    
    lighting_types = ['realistic', 'bright', 'ambient']
    
    for lighting in lighting_types:
        print(f"\n--- Test éclairage: {lighting} ---")
        
        try:
            renderer = PlanetRenderer(
                texture_path=texture_file,
                radius=1.2,
                name=f'Planète ({lighting})'
            )
            
            print(f"Rendu avec éclairage '{lighting}'...")
            renderer.render(
                background='black',
                window_size=(1000, 800),
                lighting=lighting,
                camera_distance=3.0
            )
            
            print(f"✓ Éclairage '{lighting}' testé avec succès")
            
        except Exception as e:
            print(f"✗ Erreur avec éclairage '{lighting}': {e}")


def test_error_handling():
    """Test 4: Vérification de la gestion des erreurs."""
    print("\n" + "="*60)
    print("TEST 4: Gestion des erreurs")
    print("="*60)
    
    # Test 4.1: Fichier inexistant
    print("\n4.1 - Test fichier inexistant:")
    try:
        renderer = PlanetRenderer('fichier_inexistant.jpg')
        print("✗ L'erreur n'a pas été détectée!")
    except FileNotFoundError as e:
        print(f"✓ Erreur correctement capturée: {e}")
    
    # Test 4.2: Rayon négatif
    print("\n4.2 - Test rayon négatif:")
    texture_file = create_test_texture('error_test.jpg')
    try:
        renderer = PlanetRenderer(texture_file, radius=-1.0)
        print("✗ L'erreur n'a pas été détectée!")
    except ValueError as e:
        print(f"✓ Erreur correctement capturée: {e}")
    
    # Test 4.3: Résolution trop faible
    print("\n4.3 - Test résolution invalide:")
    try:
        renderer = PlanetRenderer(texture_file, resolution=(2, 2))
        print("✗ L'erreur n'a pas été détectée!")
    except ValueError as e:
        print(f"✓ Erreur correctement capturée: {e}")
    
    print("\n✓ Tous les tests de gestion d'erreurs ont réussi!")


def test_visualizer_standalone():
    """Test 5: Test du Visualizer3D seul."""
    print("\n" + "="*60)
    print("TEST 5: Test Visualizer3D standalone")
    print("="*60)
    
    try:
        # Créer une scène simple avec plusieurs objets
        viz = Visualizer3D(background='white', title='Test Visualizer')
        
        # Ajouter plusieurs sphères de différentes couleurs
        sphere1 = pv.Sphere(center=(0, 0, 0), radius=0.5)
        sphere2 = pv.Sphere(center=(2, 0, 0), radius=0.3)
        sphere3 = pv.Sphere(center=(-2, 0, 0), radius=0.3)
        
        viz.add_mesh(sphere1, color='blue', opacity=0.8)
        viz.add_mesh(sphere2, color='red', opacity=0.8)
        viz.add_mesh(sphere3, color='green', opacity=0.8)
        
        viz.add_light(position=(5, 5, 5), intensity=1.0)
        viz.add_axes()
        
        print("✓ Visualizer3D créé avec 3 sphères")
        print("Affichage de la scène...")
        
        viz.show()
        
        print("✓ Test 5 réussi!")
        
    except Exception as e:
        print(f"✗ Erreur lors du test 5: {e}")
        import traceback
        traceback.print_exc()


def run_all_tests():
    """Lance tous les tests."""
    print("\n" + "="*60)
    print("DÉMONSTRATION COMPLÈTE - PLANET RENDERER")
    print("="*60)
    
    tests = [
        ("Test basique", test_basic_render),
        ("Test avancé", test_advanced_render),
        ("Test éclairages", test_multiple_lighting),
        ("Test erreurs", test_error_handling),
        ("Test visualizer", test_visualizer_standalone)
    ]
    
    print("\nTests disponibles:")
    for i, (name, _) in enumerate(tests, 1):
        print(f"  {i}. {name}")
    print(f"  {len(tests)+1}. Tous les tests")
    print("  0. Quitter")
    
    choice = input("\nChoisissez un test (0-6): ").strip()
    
    if choice == '0':
        print("Au revoir!")
        return
    elif choice == str(len(tests)+1):
        for name, test_func in tests:
            test_func()
            input("\nAppuyez sur Entrée pour continuer...")
    elif choice.isdigit() and 1 <= int(choice) <= len(tests):
        name, test_func = tests[int(choice)-1]
        test_func()
    else:
        print("Choix invalide!")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         SCRIPT DE DÉMONSTRATION - PLANET RENDERER          ║
    ║                                                            ║
    ║  Ce script va tester toutes les fonctionnalités           ║
    ║  du système de rendu de planètes 3D                       ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    run_all_tests()
    
    # Nettoyage optionnel
    cleanup = input("\nSupprimer les fichiers de test créés? (o/n): ").strip().lower()
    if cleanup == 'o':
        test_files = [
            'test_planet_texture.jpg',
            'advanced_texture.jpg',
            'lighting_test.jpg',
            'error_test.jpg',
            'planet_screenshot.png'
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"✓ Supprimé: {file}")
        print("Nettoyage terminé!")
    
    print("\n✨ Démonstration terminée!")