"""Class to load and interact with shaders"""

import wgpu


class Shader:
    def __init__(self, filepath: str, device: wgpu.GPUDevice) -> None:
        with open(filepath, "r") as f:
            self.source = f.read()

        self.shader = device.create_shader_module(code=self.source)
