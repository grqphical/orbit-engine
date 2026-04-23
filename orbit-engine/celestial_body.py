import numpy as np
import pygfx as gfx

class CelestialBody:
    def __init__(self, name: str, radius: float, mass: float, start_pos: np.ndarray) -> None:
        self.name = name
        self.radius = np.float64(radius)
        self.mass = np.float64(mass)
        self.position = start_pos
    
    def register_mesh(self, scale: float, scene: gfx.Scene):
        geometry = gfx.sphere_geometry(int(self.radius/scale))
        material = gfx.MeshPhongMaterial(color="#336699")
        sphere = gfx.Mesh(geometry, material)
        sphere.local.position = self.position
        scene.add(sphere)
        