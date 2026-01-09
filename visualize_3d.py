"""
visualize_3d.py
Module de visualisation 3D avec PyVista.
Fournit une classe générique pour créer des visualisations 3D interactives.
"""
import pyvista as pv
from typing import Optional, Tuple, Union
import warnings


class Visualizer3D:
    """
    Classe pour créer et gérer des visualisations 3D avec PyVista.
    
    Args:
        background (str): Couleur de fond (par défaut: 'black')
        window_size (tuple): Taille de la fenêtre en pixels (par défaut: (1024, 768))
        title (str): Titre de la fenêtre (par défaut: 'Visualisation 3D')
    
    Example:
        >>> viz = Visualizer3D(background='white')
        >>> sphere = pv.Sphere()
        >>> viz.add_mesh(sphere, color='blue')
        >>> viz.show()
    """
    
    def __init__(
        self, 
        background: str = 'black',
        window_size: Tuple[int, int] = (1024, 768),
        title: str = 'Visualisation 3D'
    ):
        self.plotter = pv.Plotter(window_size=window_size)
        self.plotter.background_color = background
        self.plotter.title = title
        self.meshes = []
        
    def add_mesh(
        self, 
        mesh: pv.DataSet, 
        texture: Optional[pv.Texture] = None,
        color: Optional[str] = None,
        opacity: float = 1.0,
        smooth_shading: bool = True,
        **kwargs
    ) -> None:
        """
        Ajoute un mesh à la scène.
        
        Args:
            mesh: Le mesh PyVista à ajouter
            texture: Texture optionnelle à appliquer
            color: Couleur du mesh (ignoré si texture fournie)
            opacity: Transparence (0.0 à 1.0)
            smooth_shading: Active le lissage de Gouraud
            **kwargs: Arguments supplémentaires pour plotter.add_mesh()
        """
        try:
            self.plotter.add_mesh(
                mesh, 
                texture=texture,
                color=color,
                opacity=opacity,
                smooth_shading=smooth_shading,
                **kwargs
            )
            self.meshes.append(mesh)
        except Exception as e:
            warnings.warn(f"Erreur lors de l'ajout du mesh: {e}")
    
    def add_light(
        self, 
        position: Tuple[float, float, float] = (5, 5, 5),
        intensity: float = 1.0,
        light_type: str = 'scene'
    ) -> None:
        """
        Ajoute une source lumineuse à la scène.
        
        Args:
            position: Position (x, y, z) de la lumière
            intensity: Intensité lumineuse (0.0 à 1.0)
            light_type: Type de lumière ('scene', 'camera', 'headlight')
        """
        try:
            light = pv.Light(position=position, light_type=light_type)
            light.intensity = intensity
            self.plotter.add_light(light)
        except Exception as e:
            warnings.warn(f"Erreur lors de l'ajout de la lumière: {e}")
    
    def set_camera(
        self,
        position: Optional[Tuple[float, float, float]] = None,
        focal_point: Tuple[float, float, float] = (0, 0, 0),
        view_up: Tuple[float, float, float] = (0, 1, 0)
    ) -> None:
        """
        Configure la position et l'orientation de la caméra.
        
        Args:
            position: Position de la caméra (x, y, z)
            focal_point: Point vers lequel la caméra regarde
            view_up: Vecteur définissant le haut de la vue
        """
        if position:
            self.plotter.camera_position = [position, focal_point, view_up]
    
    def add_axes(self, interactive: bool = True) -> None:
        """
        Ajoute des axes de référence à la scène.
        
        Args:
            interactive: Si True, ajoute un widget interactif
        """
        if interactive:
            self.plotter.add_axes()
        else:
            self.plotter.show_axes()
    
    def enable_eye_dome_lighting(self) -> None:
        """Active l'éclairage eye-dome pour améliorer la profondeur."""
        self.plotter.enable_eye_dome_lighting()
    
    def screenshot(self, filename: str, transparent_background: bool = False) -> None:
        """
        Sauvegarde une capture d'écran.
        
        Args:
            filename: Nom du fichier de sortie
            transparent_background: Fond transparent si True
        """
        try:
            self.plotter.screenshot(filename, transparent_background=transparent_background)
            print(f"Screenshot sauvegardé: {filename}")
        except Exception as e:
            warnings.warn(f"Erreur lors de la sauvegarde: {e}")
    
    def show(
        self, 
        interactive: bool = True,
        auto_close: bool = True,
        full_screen: bool = False
    ) -> None:
        """
        Affiche la visualisation.
        
        Args:
            interactive: Active les contrôles interactifs
            auto_close: Ferme automatiquement après affichage
            full_screen: Affiche en plein écran
        """
        try:
            if full_screen:
                self.plotter.full_screen = True
            
            self.plotter.show(interactive=interactive, auto_close=auto_close)
        except Exception as e:
            print(f"Erreur lors de l'affichage: {e}")
    
    def clear(self) -> None:
        """Efface tous les meshes de la scène."""
        self.plotter.clear()
        self.meshes = []
    
    def close(self) -> None:
        """Ferme le plotter et libère les ressources."""
        self.plotter.close()