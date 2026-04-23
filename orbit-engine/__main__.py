import pygfx as gfx
import numpy as np
from rendercanvas.auto import RenderCanvas, loop
from .celestial_body import CelestialBody

RENDER_SCALE = 1000.0

canvas = RenderCanvas(size=(1280, 720), title="OrbitEngine")
renderer = gfx.renderers.WgpuRenderer(canvas)

scene = gfx.Scene()

scene.add(gfx.AmbientLight())
scene.add(gfx.DirectionalLight())

camera = gfx.PerspectiveCamera(45, 1)
camera.local.z = 400

controller = gfx.FlyController(camera, speed=80, register_events=renderer)

earth = CelestialBody("Earth", 6378.0, 1000.0, np.array([0, 0, 0]))
earth.register_mesh(RENDER_SCALE, scene)

moon = CelestialBody("moon", 1737.4, 1000.0, np.array([25, 0, 0]))
moon.register_mesh(RENDER_SCALE, scene)

if __name__ == "__main__":
    canvas.request_draw(lambda: renderer.render(scene, camera))
    loop.run()
