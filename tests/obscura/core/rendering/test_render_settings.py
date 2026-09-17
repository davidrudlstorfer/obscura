"""Tests for rendering settings."""

from unittest.mock import MagicMock, patch

from obscura.core.rendering.render_settings import render


def test_render_uses_existing_settings_for_blend() -> None:
    """Test that Blender render settings are preserved."""
    mock_scene = MagicMock()
    mock_scene.render.engine = "BLENDER_EEVEE_NEXT"
    mock_scene.render.resolution_x = 1920
    mock_scene.render.resolution_y = 1080
    mock_scene.render.image_settings.file_format = "OPEN_EXR"

    mock_config = MagicMock()
    mock_config.general.input_file_path = "/fake/scene.blend"
    mock_config.general.output_file_path = "/fake/output.png"

    with (
        patch("obscura.core.rendering.render_settings.bpy") as mock_bpy,
        patch(
            "obscura.core.rendering.render_settings._configure_render_device"
        ) as mock_configure_device,
    ):
        render(mock_scene, mock_config)

        assert mock_scene.render.filepath == "/fake/output.png"
        assert mock_scene.render.engine == "BLENDER_EEVEE_NEXT"
        assert mock_scene.render.resolution_x == 1920
        assert mock_scene.render.resolution_y == 1080
        assert mock_scene.render.image_settings.file_format == "OPEN_EXR"
        mock_configure_device.assert_not_called()
        mock_bpy.ops.render.render.assert_called_once_with(write_still=True)


def test_render_configures_cycles_device_for_blend() -> None:
    """Test that Cycles device configuration is applied for Blender files."""
    mock_scene = MagicMock()
    mock_scene.render.engine = "CYCLES"
    mock_scene.cycles.samples = 64

    mock_config = MagicMock()
    mock_config.general.input_file_path = "/fake/scene.blend"
    mock_config.general.output_file_path = "/fake/output.png"

    with (
        patch("obscura.core.rendering.render_settings.bpy") as mock_bpy,
        patch(
            "obscura.core.rendering.render_settings._configure_render_device"
        ) as mock_configure_device,
    ):
        render(mock_scene, mock_config)

        assert mock_scene.render.filepath == "/fake/output.png"
        assert mock_scene.cycles.samples == 64
        mock_configure_device.assert_called_once_with(mock_scene)
        mock_bpy.ops.render.render.assert_called_once_with(write_still=True)
