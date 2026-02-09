"""Rendering settings and final image generation in Blender."""

import os
from typing import Any

import bpy


def render(scene: bpy.types.Scene, config: Any) -> None:
    """Configure preview or full render settings."""
    output_path = config.general.output_file_path
    scene.render.image_settings.file_format = "PNG"

    preview = config.render.preview.mode

    if preview:
        base, ext = os.path.splitext(output_path)
        scene.render.filepath = f"{base}_preview{ext}"
        scene.render.resolution_x = config.render.preview.resolution_x
        scene.render.resolution_y = config.render.preview.resolution_y
        scene.render.engine = config.render.preview.engine
        if scene.render.engine == "CYCLES":
            scene.cycles.samples = config.render.preview.samples
            scene.cycles.use_denoising = config.render.preview.use_denoising
        # Eevee Next has no configurable preview effects

    else:
        scene.render.filepath = output_path
        scene.render.resolution_x = config.render.resolution_x
        scene.render.resolution_y = config.render.resolution_y
        scene.render.engine = config.render.engine
        if scene.render.engine == "CYCLES":
            scene.cycles.samples = config.render.samples
            scene.cycles.use_denoising = True

    # Render
    bpy.ops.render.render(write_still=True)
