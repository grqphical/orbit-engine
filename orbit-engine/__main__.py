"""
Orbit Engine
"""

import wgpu
import logging
from rendercanvas.auto import RenderCanvas, loop

WIDTH, HEIGHT = 1280, 720


def get_render_pipeline(canvas, device: wgpu.GPUDevice):
    with open("shaders/basic_shader.wgsl", "r") as f:
        shader_src = f.read()
    shader = device.create_shader_module(code=shader_src)

    pipeline_layout = device.create_pipeline_layout(bind_group_layouts=[])

    present_context = canvas.get_context("wgpu")
    render_texture_format = present_context.get_preferred_format(device.adapter)
    present_context.configure(device=device, format=render_texture_format)

    return device.create_render_pipeline(
        layout=pipeline_layout,
        vertex={
            "module": shader,
            "entry_point": "vs_main",
        },
        primitive={
            "topology": wgpu.PrimitiveTopology.triangle_list,
            "front_face": wgpu.FrontFace.ccw,
            "cull_mode": wgpu.CullMode.none,
        },
        depth_stencil=None,
        multisample=None,
        fragment={
            "module": shader,
            "entry_point": "fs_main",
            "targets": [
                {
                    "format": render_texture_format,
                    "blend": {
                        "color": {},
                        "alpha": {},
                    },
                },
            ],
        },
    )


def get_draw_function(canvas, device, render_pipeline):
    def draw_frame():
        current_texture = canvas.get_context("wgpu").get_current_texture()
        command_encoder = device.create_command_encoder()

        render_pass = command_encoder.begin_render_pass(
            color_attachments=[
                {
                    "view": current_texture.create_view(),
                    "resolve_target": None,
                    "clear_value": (0, 0, 0, 1),
                    "load_op": wgpu.LoadOp.clear,
                    "store_op": wgpu.StoreOp.store,
                }
            ],
        )

        render_pass.set_pipeline(render_pipeline)
        # render_pass.set_bind_group(0, no_bind_group)
        render_pass.draw(3, 1, 0, 0)
        render_pass.end()
        device.queue.submit([command_encoder.finish()])

    return draw_frame


def setup_drawing_sync(canvas, power_preference="high-performance", limits=None):
    """Regular function to set up a viz on the given canvas."""

    adapter = wgpu.gpu.request_adapter_sync(power_preference=power_preference)
    device = adapter.request_device_sync(required_limits=limits)

    render_pipeline = get_render_pipeline(canvas, device)

    return get_draw_function(canvas, device, render_pipeline)


if __name__ == "__main__":
    logger = logging.getLogger("wgpu")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    canvas = RenderCanvas(title="OrbitEngine", size=(WIDTH, HEIGHT))

    adapter = wgpu.gpu.request_adapter_sync(power_preference="high-performance")
    device = adapter.request_device_sync()

    render_pipeline = get_render_pipeline(canvas, device)

    canvas.request_draw(get_draw_function(canvas, device, render_pipeline))

    loop.run()
