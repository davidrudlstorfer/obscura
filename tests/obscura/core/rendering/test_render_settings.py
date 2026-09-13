"""Tests for rendering settings."""

from unittest.mock import MagicMock, patch

from obscura.core.rendering.render_settings import render_blend


def test_render_blend_uses_existing_render_settings() -> None:
    """Test that Blender render settings are preserved."""
    mock_scene = MagicMock()
    mock_config = MagicMock()
    mock_config.general.output_file_path = "/fake/output.png"

    with patch("obscura.core.rendering.render_settings.bpy") as mock_bpy:
        render_blend(mock_scene, mock_config)

        assert mock_scene.render.filepath == "/fake/output.png"
        mock_bpy.ops.render.render.assert_called_once_with(write_still=True)
