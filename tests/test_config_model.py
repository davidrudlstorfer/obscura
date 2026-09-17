"""Tests for Obscura configuration models."""

from pathlib import Path

import yaml

from obscura.core.config_model import Configuration

CONFIG_PATH = Path(__file__).parents[1] / "src" / "obscura" / "configs" / "params.yaml"


def test_config_model():
    """Test that the YAML configuration can be validated into a Configuration
    model."""
    with CONFIG_PATH.open("r") as file:
        data = yaml.safe_load(file)

    config = Configuration.model_validate(data)

    assert isinstance(config, Configuration)


def test_blend_config_model():
    """Test that a Blender configuration only requires general settings."""
    data = {
        "general": {
            "output_directory": "output",
            "sim_name": "test_sim",
            "log_file": "obscura.log",
            "log_to_console": True,
            "input_file_path": "/fake/scene.blend",
            "output_file_path": "/fake/output.png",
        }
    }

    config = Configuration.model_validate(data)

    assert isinstance(config, Configuration)
    assert config.render is None
    assert config.object_settings is None
    assert config.material is None
    assert config.light is None
    assert config.camera is None
