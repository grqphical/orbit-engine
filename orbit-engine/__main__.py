"""
Orbit Engine
"""
from .rendering import setup_drawing_sync

if __name__ == "__main__":
    from rendercanvas.auto import RenderCanvas, loop

    canvas = RenderCanvas(size=(640, 480), title="Orbit Engine")
    context = canvas.get_wgpu_context()

    draw_frame = setup_drawing_sync(context)
    canvas.request_draw(draw_frame)
    loop.run()
