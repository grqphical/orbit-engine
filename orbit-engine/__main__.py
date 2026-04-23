import pygfx as gfx
from rendercanvas.auto import RenderCanvas, loop

canvas = RenderCanvas(size=(1280, 720), title="OrbitEngine")
renderer = gfx.renderers.WgpuRenderer(canvas)

scene = gfx.Scene()

scene.add(gfx.AmbientLight())
scene.add(gfx.DirectionalLight())

camera = gfx.PerspectiveCamera(45, 1)
camera.local.z = 400

controller = gfx.FlyController(camera, speed=80, register_events=renderer)

geometry = gfx.box_geometry(200, 200, 200)
material = gfx.MeshPhongMaterial(color="#336699")
cube = gfx.Mesh(geometry, material)
scene.add(cube)

if __name__ == "__main__":
    canvas.request_draw(lambda: renderer.render(scene, camera))
    loop.run()
