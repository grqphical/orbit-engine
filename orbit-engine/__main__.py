"""
Orbit Engine
"""

import wgpu
import logging
import sys
from rendercanvas.auto import RenderCanvas, loop

WIDTH, HEIGHT = 1280, 720

if __name__ == "__main__":
    logger = logging.getLogger("wgpu")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    canvas = RenderCanvas(title="OrbitEngine", size=(WIDTH, HEIGHT))

    adapter = wgpu.gpu.request_adapter_sync(power_preference="high-performance")
    device = adapter.request_device_sync()

    present_context = canvas.get_wgpu_context()
    render_texture_format = present_context.get_preferred_format(device.adapter)
    present_context.configure(device=device, format=render_texture_format)

    loop.run()
