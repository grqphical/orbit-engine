"""
Script responsible for the rendering of 3D objects using WGPU
"""

from typing import Callable
from .shader import Shader
import wgpu


def setup_drawing_sync(
    context, power_preference="high-performance", limits=None, format=None
) -> Callable:
    """Setup to draw a triangle on the given context.

    Returns the draw function.
    """

    adapter = wgpu.gpu.request_adapter_sync(power_preference=power_preference)
    device = adapter.request_device_sync(required_limits=limits)

    pipeline_kwargs = get_render_pipeline_kwargs(context, device, format)

    render_pipeline = device.create_render_pipeline(**pipeline_kwargs)

    return get_draw_function(context, device, render_pipeline)


def get_render_pipeline_kwargs(
    context, device: wgpu.GPUDevice, render_texture_format
) -> wgpu.RenderPipelineDescriptor:
    if render_texture_format is None:
        render_texture_format = context.get_preferred_format(device.adapter)
    context.configure(device=device, format=render_texture_format)

    shader = Shader("shaders/basic_shader.wgsl", device)
    pipeline_layout = device.create_pipeline_layout(bind_group_layouts=[])

    return wgpu.RenderPipelineDescriptor(
        layout=pipeline_layout,
        vertex=wgpu.VertexState(
            module=shader.shader,
            entry_point="vs_main",
        ),
        depth_stencil=None,
        multisample=None,
        fragment=wgpu.FragmentState(
            module=shader.shader,
            entry_point="fs_main",
            targets=[
                wgpu.ColorTargetState(
                    format=render_texture_format,
                    blend={"color": {}, "alpha": {}},
                )
            ],
        ),
    )


def get_draw_function(
    context,
    device: wgpu.GPUDevice,
    render_pipeline: wgpu.GPURenderPipeline,
) -> Callable:
    def draw_frame_sync():
        current_texture = context.get_current_texture()
        command_encoder = device.create_command_encoder()

        render_pass = command_encoder.begin_render_pass(
            color_attachments=[
                wgpu.RenderPassColorAttachment(
                    view=current_texture.create_view(),
                    resolve_target=None,
                    clear_value=(0, 0, 0, 1),
                    load_op="clear",
                    store_op="store",
                )
            ],
        )

        render_pass.set_pipeline(render_pipeline)
        # render_pass.set_bind_group(0, no_bind_group)
        render_pass.draw(3, 1, 0, 0)
        render_pass.end()
        device.queue.submit([command_encoder.finish()])

    return draw_frame_sync
