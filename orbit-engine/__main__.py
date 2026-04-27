import pygfx as gfx
import numpy as np
from rendercanvas.auto import RenderCanvas, loop
from .celestial_body import CelestialBody
from imgui_bundle import imgui, imgui_ctx
from wgpu.utils.imgui import ImguiRenderer

RENDER_SCALE = 1000.0
DISTANCE_SCALE = 6378.0

def imgui_loop():
    imgui.set_next_window_size((300, 0), imgui.Cond_.appearing)
    imgui.set_next_window_pos((0, 20), imgui.Cond_.appearing)

    imgui.begin("Custom window", None)
    imgui.text("Example Text")

    if imgui.button("Hello"):
        print("World")
    imgui.end()

canvas = RenderCanvas(size=(1280, 720), title="OrbitEngine")
renderer = gfx.renderers.WgpuRenderer(canvas)

imgui_renderer = ImguiRenderer(device=renderer.device, canvas=canvas)

scene = gfx.Scene()

scene.add(gfx.AmbientLight())
scene.add(gfx.DirectionalLight())

camera = gfx.PerspectiveCamera(45, 1)
camera.local.z = 400

controller = gfx.FlyController(camera, speed=80, register_events=renderer)

earth = CelestialBody("Earth", 6378.0, 1000.0, np.array([0, 0, 0]))
earth.register_mesh(RENDER_SCALE, scene)

moon = CelestialBody("moon", 1737.4, 1000.0, np.array([384784 / DISTANCE_SCALE, 0, 0]))
moon.register_mesh(RENDER_SCALE, scene)

imgui_renderer.set_gui(imgui_loop)

def render_loop():
    renderer.render(scene, camera)
    imgui_renderer.render()

    canvas.request_draw()
    

if __name__ == "__main__":
    canvas.request_draw(render_loop)
    loop.run()
