import pygfx as gfx
from rendercanvas.auto import RenderCanvas

canvas = RenderCanvas(size=(1280, 720), title="OrbitEngine")

scene = gfx.Scene()

scene.add(gfx.AmbientLight())
scene.add(gfx.DirectionalLight())

camera = gfx.PerspectiveCamera(45, 16 / 9)
camera.local.z = 400
scene.add(camera)

geometry = gfx.box_geometry(200, 200, 200)
material = gfx.MeshPhongMaterial(color="#336699")
cube = gfx.Mesh(geometry, material)
scene.add(cube)

camera.show_object(cube, view_dir=(-1, -1, -1), match_aspect=True)

if __name__ == "__main__":
    gfx.show(scene, canvas=canvas)
