"""Pydantic models for Obscura configuration."""

from pydantic import BaseModel


class General(BaseModel):
    """General application configuration."""

    output_directory: str
    sim_name: str
    log_file: str
    log_to_console: bool
    input_file_path: str
    output_file_path: str


class ObjectSettings(BaseModel):
    """Configuration for the rendered object."""

    mesh_scale: list[float]
    mesh_location: list[float]
    rotation: list[int]


class Material(BaseModel):
    """Material properties used for rendering."""

    material_color: list[float]
    material_roughness: float
    material_metallic: float


class Light(BaseModel):
    """Lighting configuration."""

    key_light_intensity: float
    fill_light_intensity: float
    ambient_light_strength: float


class Camera(BaseModel):
    """Camera configuration."""

    lens: int
    type: str


class Preview(BaseModel):
    """Preview rendering settings."""

    mode: bool
    resolution_x: int
    resolution_y: int
    engine: str
    samples: int
    use_denoising: bool


class Render(BaseModel):
    """Final rendering configuration."""

    preview: Preview
    resolution_x: int
    resolution_y: int
    engine: str
    samples: int


class Configuration(BaseModel):
    """Root configuration model for Obscura."""

    general: General
    object_settings: ObjectSettings
    background_color: list[float]
    material: Material
    light: Light
    camera: Camera
    render: Render


class BlendConfiguration(BaseModel):
    """Configuration for rendering a Blender file."""

    general: General
    render: Render
