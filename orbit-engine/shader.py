from pathlib import Path
import wgpu


class Shader:
    """Used to easily load shaders from WGSL files"""

    def __init__(self, path: str | Path, device: wgpu.GPUDevice) -> None:
        self.path = Path(path)
        self.source = self.path.read_text(encoding="utf-8")

        self.module = device.create_shader_module(
            label=self.path.name,
            code=self.source,
        )
