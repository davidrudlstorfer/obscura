"""Test rendering pipeline."""

from unittest.mock import MagicMock, patch

from obscura.core.rendering.rendering_pipeline import rendering_pipeline


def test_rendering_pipeline_calls_all_steps() -> None:
    """Test that rendering pipeline calls all steps in correct order."""

    mock_config = MagicMock()
    mock_mesh = MagicMock()
    mock_center = (0, 0, 0)
    mock_extent = 10.0

    # mock scene and filepath
    mock_scene = MagicMock()
    mock_scene.render.filepath = "/fake/output.png"

    with (
        patch("obscura.core.rendering.rendering_pipeline.bpy") as mock_bpy,
        patch(
            "obscura.core.rendering.rendering_pipeline.load_mesh",
            return_value=mock_mesh,
        ) as mock_load_mesh,
        patch(
            "obscura.core.rendering.rendering_pipeline.apply_transforms"
        ) as mock_apply_transforms,
        patch(
            "obscura.core.rendering.rendering_pipeline.compute_geometry",
            return_value=(mock_center, mock_extent),
        ) as mock_compute_geometry,
        patch(
            "obscura.core.rendering.rendering_pipeline.setup_camera"
        ) as mock_setup_camera,
        patch(
            "obscura.core.rendering.rendering_pipeline.define_background"
        ) as mock_define_background,
        patch(
            "obscura.core.rendering.rendering_pipeline.ambient_lighting"
        ) as mock_ambient_lighting,
        patch(
            "obscura.core.rendering.rendering_pipeline.setup_lighting"
        ) as mock_setup_lighting,
        patch(
            "obscura.core.rendering.rendering_pipeline.apply_material"
        ) as mock_apply_material,
        patch("obscura.core.rendering.rendering_pipeline.render") as mock_render,
    ):
        # configure bpy scene
        mock_bpy.context.scene = mock_scene

        # run pipeline
        rendering_pipeline(mock_config)

        # scene reset
        mock_bpy.ops.wm.read_factory_settings.assert_called_once_with(use_empty=True)

        # mesh handling
        mock_load_mesh.assert_called_once_with(mock_config)
        mock_apply_transforms.assert_called_once_with(mock_mesh, mock_config)
        mock_compute_geometry.assert_called_once_with(mock_mesh)

        # camera
        mock_setup_camera.assert_called_once_with(
            mock_config, mock_mesh, mock_center, mock_extent
        )

        # background & lighting
        mock_define_background.assert_called_once_with(mock_config)
        mock_ambient_lighting.assert_called_once_with(mock_config)
        mock_setup_lighting.assert_called_once_with(
            mock_center, mock_extent, mock_config
        )

        # material
        mock_apply_material.assert_called_once_with(mock_mesh, mock_config)

        # render
        mock_render.assert_called_once_with(mock_scene, mock_config)
