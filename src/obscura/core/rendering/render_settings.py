"""Rendering settings and final image generation in Blender."""

import os
from typing import Any

import bpy


def render(scene: bpy.types.Scene, config: Any) -> None:
    """Configure preview or full render settings."""
    output_path = config.paths.output_file
    scene.render.image_settings.file_format = "PNG"

    preview = config.preview.preview_mode

    if preview:
        base, ext = os.path.splitext(output_path)
        scene.render.filepath = f"{base}_preview{ext}"
        scene.render.resolution_x = config.preview.preview_resolution_x
        scene.render.resolution_y = config.preview.preview_resolution_y
        scene.render.engine = config.preview.preview_engine
        if scene.render.engine == "CYCLES":
            scene.cycles.samples = config.preview.preview_samples
            scene.cycles.use_denoising = config.preview.preview_use_denoising
        # Eevee Next has no configurable preview effects

    else:
        scene.render.filepath = output_path
        scene.render.resolution_x = config.render.render_resolution_x
        scene.render.resolution_y = config.render.render_resolution_y
        scene.render.engine = config.render.render_engine
        if scene.render.engine == "CYCLES":
            scene.cycles.samples = config.render.samples
            scene.cycles.use_denoising = True

    # Render
    bpy.ops.render.render(write_still=True)
