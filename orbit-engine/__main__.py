import wgpu
import glm
import logging
import numpy as np

from .shader import Shader
from rendercanvas.auto import RenderCanvas, loop

WIDTH, HEIGHT = 1280, 720


def get_render_pipeline(canvas, device: wgpu.GPUDevice, pipeline_layout):
    shader = Shader("shaders/basic_shader.wgsl", device)

    present_context = canvas.get_context("wgpu")
    render_texture_format = present_context.get_preferred_format(device.adapter)
    present_context.configure(device=device, format=render_texture_format)

    return device.create_render_pipeline(
        layout=pipeline_layout,
        vertex={
            "module": shader.module,
            "entry_point": "vs_main",
            "buffers": [],
        },
        primitive={
            "topology": wgpu.PrimitiveTopology.triangle_list,
            "front_face": wgpu.FrontFace.ccw,
            "cull_mode": wgpu.CullMode.none,
        },
        fragment={
            "module": shader.module,
            "entry_point": "fs_main",
            "targets": [
                {
                    "format": render_texture_format,
                    "blend": {
                        "color": {
                            "src_factor": "src-alpha",
                            "dst_factor": "one-minus-src-alpha",
                        },
                        "alpha": {"src_factor": "one", "dst_factor": "zero"},
                    },
                },
            ],
        },
    )


def get_draw_function(canvas, device: wgpu.GPUDevice, render_pipeline, bind_group):
    def draw_frame():
        current_texture = canvas.get_context("wgpu").get_current_texture()
        command_encoder = device.create_command_encoder()

        render_pass = command_encoder.begin_render_pass(
            color_attachments=[
                {
                    "view": current_texture.create_view(),
                    "resolve_target": None,
                    "clear_value": (0.05, 0.05, 0.05, 1),  # Dark grey background
                    "load_op": wgpu.LoadOp.clear,
                    "store_op": wgpu.StoreOp.store,
                }
            ],
        )

        render_pass.set_pipeline(render_pipeline)
        render_pass.set_bind_group(0, bind_group)
        render_pass.draw(3, 1, 0, 0)
        render_pass.end()
        device.queue.submit([command_encoder.finish()])

    return draw_frame


def setup_drawing_sync(canvas):
    adapter = wgpu.gpu.request_adapter_sync(power_preference="high-performance")
    device = adapter.request_device_sync()

    proj = glm.perspectiveRH_ZO(glm.radians(45), WIDTH / HEIGHT, 0.1, 100.0)
    view = glm.lookAt(glm.vec3(0, 0, -3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    model = glm.rotate(glm.mat4(1.0), glm.radians(-55), glm.vec3(1, 0, 0))

    view_proj = proj * view
    view_proj_model_data = np.concatenate(
        [
            np.array(view_proj, dtype=np.float32).flatten(),
            np.array(model, dtype=np.float32).flatten(),
        ]
    ).tobytes()

    matrix_size = 64 * 2
    uniform_buffer = device.create_buffer(
        size=matrix_size, usage=wgpu.BufferUsage.UNIFORM | wgpu.BufferUsage.COPY_DST
    )
    device.queue.write_buffer(uniform_buffer, 0, view_proj_model_data)

    bind_group_layout = device.create_bind_group_layout(
        entries=[
            {
                "binding": 0,
                "visibility": wgpu.ShaderStage.VERTEX,
                "buffer": {"type": wgpu.BufferBindingType.uniform},
            }
        ]
    )

    pipeline_layout = device.create_pipeline_layout(
        bind_group_layouts=[bind_group_layout]
    )

    bind_group = device.create_bind_group(
        layout=bind_group_layout,
        entries=[
            {
                "binding": 0,
                "resource": {
                    "buffer": uniform_buffer,
                    "offset": 0,
                    "size": matrix_size,
                },
            }
        ],
    )

    render_pipeline = get_render_pipeline(canvas, device, pipeline_layout)
    return get_draw_function(canvas, device, render_pipeline, bind_group)


if __name__ == "__main__":
    logger = logging.getLogger("wgpu")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    canvas = RenderCanvas(title="OrbitEngine", size=(WIDTH, HEIGHT))

    draw_fn = setup_drawing_sync(canvas)
    canvas.request_draw(draw_fn)

    loop.run()
