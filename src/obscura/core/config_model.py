"""Pydantic models for Obscura configuration."""
from pydantic import BaseModel

# Create a Pydantic model for validating customer support input
class General(BaseModel):
    output_directory: str
    sim_name: str
    log_file: str
    log_to_console: bool
    input_file_path: str
    output_file_path: str


class ObjectSettings(BaseModel):
    mesh_scale: list[float]
    mesh_location: list[float]
    rotation: list[int]


class Material(BaseModel):
    material_color: list[float]
    material_roughness: float
    material_metallic: float


class Light(BaseModel):
    key_light_intensity: float
    fill_light_intensity: float
    ambient_light_strength: float


class Camera(BaseModel):
    lens: int
    type: str


class Preview(BaseModel):
    mode: bool
    resolution_x: int
    resolution_y: int
    engine: str
    samples: int
    use_denoising: bool


class Render(BaseModel):
    preview: Preview
    resolution_x: int
    resolution_y: int
    engine: str
    samples: int


class Configuration(BaseModel):
    general: General
    object_settings: ObjectSettings
    background_color: list[float]
    material: Material
    light: Light
    camera: Camera
    render: Render