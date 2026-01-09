"""
Module de rendu de planètes en 3D.
Utilise PyVista pour créer des visualisations réalistes de planètes avec textures.
"""
import pyvista as pv
import os
from typing import Optional, Tuple
from visualize_3d import Visualizer3D


class PlanetRenderer:
    """
    Classe pour le rendu 3D de planètes avec textures.
    
    Args:
        texture_path (str): Chemin vers le fichier de texture
        radius (float): Rayon de la planète (par défaut: 1.0)
        resolution (tuple): Résolution (theta, phi) de la sphère (par défaut: (256, 128))
        name (str): Nom de la planète (par défaut: 'Planet')
    
    Raises:
        FileNotFoundError: Si le fichier de texture n'existe pas
        ValueError: Si les paramètres sont invalides
    
    Example:
        >>> renderer = PlanetRenderer('earth_texture.jpg', radius=1.5)
        >>> renderer.render(rotation_speed=5.0, show_axes=True)
    """
    
    def __init__(
        self,
        texture_path: str,
        radius: float = 1.0,
        resolution: Tuple[int, int] = (256, 128),
        name: str = 'Planet'
    ):
        self.texture_path = texture_path
        self.radius = radius
        self.theta_resolution, self.phi_resolution = resolution
        self.name = name
        
        # Validation
        self._validate_parameters()
    
    def _validate_parameters(self) -> None:
        """Valide les paramètres d'initialisation."""
        if not os.path.exists(self.texture_path):
            raise FileNotFoundError(
                f"Texture non trouvée: {self.texture_path}\n"
                f"Vérifiez que le chemin est correct."
            )
        
        if self.radius <= 0:
            raise ValueError(f"Le rayon doit être positif (reçu: {self.radius})")
        
        if self.theta_resolution < 3 or self.phi_resolution < 3:
            raise ValueError(
                f"Résolution trop faible: ({self.theta_resolution}, {self.phi_resolution}). "
                f"Minimum: (3, 3)"
            )
    
    def _create_sphere(self) -> pv.PolyData:
        """
        Crée la géométrie sphérique de la planète.
        
        Returns:
            pv.PolyData: Mesh de la sphère
        """
        sphere = pv.Sphere(
            radius=self.radius,
            theta_resolution=self.theta_resolution,
            phi_resolution=self.phi_resolution,
            start_theta=0,
            end_theta=360,
            start_phi=0,
            end_phi=180
        )
        return sphere
    
    def _load_texture(self) -> pv.Texture:
        """
        Charge la texture de la planète.
        
        Returns:
            pv.Texture: Texture chargée
        
        Raises:
            RuntimeError: Si le chargement échoue
        """
        try:
            texture = pv.read_texture(self.texture_path)
            return texture
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement de la texture: {e}")
    
    def render(
        self,
        background: str = 'black',
        window_size: Tuple[int, int] = (1200, 900),
        lighting: str = 'realistic',
        rotation_speed: Optional[float] = None,
        show_axes: bool = False,
        camera_distance: float = 3.0,
        save_screenshot: Optional[str] = None,
        enable_anti_aliasing: bool = True
    ) -> None:
        """
        Effectue le rendu 3D de la planète.
        
        Args:
            background: Couleur de fond ('black', 'white', 'space', etc.)
            window_size: Dimensions de la fenêtre (largeur, hauteur)
            lighting: Type d'éclairage ('realistic', 'bright', 'ambient')
            rotation_speed: Vitesse de rotation (None = pas de rotation)
            show_axes: Affiche les axes de référence
            camera_distance: Distance de la caméra par rapport à la planète
            save_screenshot: Chemin pour sauvegarder une capture (None = pas de sauvegarde)
            enable_anti_aliasing: Active l'anti-aliasing pour un meilleur rendu
        """
        # Création du visualiseur
        visualizer = Visualizer3D(
            background=background,
            window_size=window_size,
            title=f'Rendu 3D - {self.name}'
        )
        
        # Création de la sphère et chargement de la texture
        sphere = self._create_sphere()
        texture = self._load_texture()
        
        # Ajout du mesh
        visualizer.add_mesh(
            sphere,
            texture=texture,
            smooth_shading=True
        )
        
        # Configuration de l'éclairage
        self._setup_lighting(visualizer, lighting)
        
        # Configuration de la caméra
        camera_position = (0, 0, self.radius * camera_distance)
        visualizer.set_camera(
            position=camera_position,
            focal_point=(0, 0, 0),
            view_up=(0, 1, 0)
        )
        
        # Options supplémentaires
        if show_axes:
            visualizer.add_axes(interactive=True)
        
        if enable_anti_aliasing:
            visualizer.enable_eye_dome_lighting()
        
        # Rotation (si demandée)
        if rotation_speed is not None:
            self._add_rotation(visualizer, rotation_speed)
        
        # Sauvegarde screenshot
        if save_screenshot:
            visualizer.screenshot(save_screenshot)
        
        # Affichage
        visualizer.show()
    
    def _setup_lighting(self, visualizer: Visualizer3D, lighting_type: str) -> None:
        """
        Configure l'éclairage de la scène.
        
        Args:
            visualizer: Instance du visualiseur
            lighting_type: Type d'éclairage à appliquer
        """
        if lighting_type == 'realistic':
            # Lumière principale (soleil)
            visualizer.add_light(
                position=(5, 3, 5),
                intensity=1.2
            )
            # Lumière d'ambiance douce
            visualizer.add_light(
                position=(-3, -2, 3),
                intensity=0.3
            )
        
        elif lighting_type == 'bright':
            visualizer.add_light(
                position=(5, 5, 5),
                intensity=1.5
            )
            visualizer.add_light(
                position=(-5, -5, 5),
                intensity=0.8
            )
        
        elif lighting_type == 'ambient':
            visualizer.add_light(
                position=(0, 0, 5),
                intensity=0.8
            )
        
        else:
            # Éclairage par défaut
            visualizer.add_light(
                position=(5, 5, 5),
                intensity=1.0
            )
    
    def _add_rotation(self, visualizer: Visualizer3D, speed: float) -> None:
        """
        Ajoute une rotation animée à la planète.
        
        Args:
            visualizer: Instance du visualiseur
            speed: Vitesse de rotation en degrés par frame
        """
        # Note: Cette fonctionnalité nécessiterait une boucle d'animation
        # Pour PyVista, cela peut être implémenté avec plotter.add_timer_event
        # ou en utilisant un callback personnalisé
        print(f"Rotation à {speed}°/s (fonctionnalité à implémenter avec callbacks)")


# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple basique
    try:
        renderer = PlanetRenderer(
            texture_path='earth_texture.jpg',
            radius=1.5,
            resolution=(512, 256),
            name='Terre'
        )
        
        renderer.render(
            background='space',
            lighting='realistic',
            show_axes=True,
            camera_distance=2.5,
            enable_anti_aliasing=True
        )
    
    except FileNotFoundError as e:
        print(f"Erreur: {e}")
        print("Assurez-vous d'avoir un fichier de texture valide.")
    except Exception as e:
        print(f"Erreur inattendue: {e}")