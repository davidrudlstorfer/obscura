"""Test utilities."""

import os
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from obscura.core.config_model import Configuration
from obscura.core.utilities import RunManager


def test_run_manager_init_run() -> None:
    """Test run manager init_run function."""
    mock_config = MagicMock()

    with (
        patch("obscura.core.utilities.setup_logging") as mock_setup_logging,
        patch("obscura.core.utilities.print_header") as mock_print_header,
        patch("obscura.core.utilities.log_full_width") as mock_log_full_width,
        patch("obscura.core.utilities.RunManager.write_config") as mock_write_config,
    ):
        run_manager = RunManager(mock_config)

        run_manager.init_run()

        mock_setup_logging.assert_called_once_with(
            mock_config.general.log_to_console,
            mock_config.general.log_file,
            mock_config.general.output_directory,
            mock_config.general.sim_name,
            "obscura",
        )
        mock_print_header.assert_called_once_with(
            title="Obscura",
            description="General Python Skeleton",
        )
        mock_log_full_width.assert_called_once_with("RUN STARTED")
        mock_write_config.assert_called_once()


def test_write_config(tmp_path: Path) -> None:
    """Test write_config function.

    Args:
        tmp_path (Path): Temporary directory from pytest.
    """
    mock_config = Configuration(
        general={
            "output_directory": str(tmp_path),
            "sim_name": "sim_name",
            "log_file": "test.log",
            "log_to_console": True,
            "input_file_path": "input.stl",
            "output_file_path": "output.png",
        },
        object_settings={
            "mesh_scale": [1.0, 1.0, 1.0],
            "mesh_location": [0.0, 0.0, 0.0],
            "rotation": [0, 0, 0],
        },
        background_color=[1.0, 1.0, 1.0, 1.0],
        material={
            "material_color": [0.07, 0.28, 0.55, 1.0],
            "material_roughness": 0.5,
            "material_metallic": 0.0,
        },
        light={
            "key_light_intensity": 3.0,
            "fill_light_intensity": 1.25,
            "ambient_light_strength": 0.2,
        },
        camera={
            "lens": 35,
            "type": "PERSP",
        },
        render={
            "preview": {
                "mode": False,
                "resolution_x": 960,
                "resolution_y": 600,
                "engine": "CYCLES",
                "samples": 32,
                "use_denoising": True,
            },
            "resolution_x": 1920,
            "resolution_y": 1200,
            "engine": "CYCLES",
            "samples": 128,
        },
    )

    run_manager = RunManager(mock_config)

    run_manager.write_config()

    config_path = os.path.join(
        tmp_path,
        "sim_name",
        "config.yaml",
    )

    with open(config_path, "r") as file:
        assert yaml.safe_load(file) == mock_config.model_dump()

    # Check invalid input parameter combination.
    invalid_config = mock_config.model_copy(
        update={
            "general": mock_config.general.model_copy(
                update={
                    "output_directory": None,
                    "sim_name": None,
                }
            )
        }
    )

    run_manager = RunManager(invalid_config)

    with pytest.raises(
        ValueError,
        match="Output directory and sim name must be provided for output!",
    ):
        run_manager.write_config()


def test_run_manager_finish_run() -> None:
    """Test run manager finish_run function."""
    mock_config = MagicMock()

    with (
        patch("obscura.core.utilities.log_full_width") as mock_log_full_width,
        patch("obscura.core.utilities.log") as mock_log,
    ):
        run_manager = RunManager(mock_config)

        run_manager.finish_run(start_time=time.time())

        mock_log_full_width.assert_called_with("RUN FINISHED")
        mock_log.info.assert_called_once()
