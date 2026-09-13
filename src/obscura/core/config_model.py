"""Pydantic models for Obscura configuration."""

from pathlib import Path

from pydantic import BaseModel, model_validator


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
    object_settings: ObjectSettings | None = None
    background_color: list[float] | None = None
    material: Material | None = None
    light: Light | None = None
    camera: Camera | None = None
    render: Render | None = None

    @model_validator(mode="after")  # type: ignore[untyped-decorator]
    def validate_required_settings(self) -> "Configuration":
        """Require rendering settings for non-Blender input files."""
        if Path(self.general.input_file_path).suffix.lower() != ".blend":
            required_fields = [
                "object_settings",
                "background_color",
                "material",
                "light",
                "camera",
                "render",
            ]

            missing_fields = [
                field for field in required_fields if getattr(self, field) is None
            ]

            if missing_fields:
                raise ValueError(
                    "Missing required configuration fields: "
                    + ", ".join(missing_fields)
                )

        return self
