"""Rendering settings and final image generation in Blender."""

import os
from typing import Any

import bpy


def render(scene: bpy.types.Scene, config: Any) -> None:
    """Configure preview or full render settings."""
    output_path = config.paths.output_file
    scene.render.image_settings.file_format = "PNG"

    preview = config.preview.get("preview_mode", False)  # Deactivated by default

    if preview:
        base, ext = os.path.splitext(output_path)
        scene.render.filepath = f"{base}_preview{ext}"
        scene.render.resolution_x = config.preview.get("preview_resolution_x", 640)
        scene.render.resolution_y = config.preview.get("preview_resolution_y", 360)
        scene.render.engine = config.preview.get("preview_engine", "BLENDER_EEVEE_NEXT")
        if scene.render.engine == "CYCLES":
            scene.cycles.samples = config.preview.get("preview_samples", 8)
            scene.cycles.use_denoising = config.preview.get(
                "preview_use_denoising", True
            )

    else:
        scene.render.filepath = output_path
        scene.render.resolution_x = config.render.get("render_resolution_x", 1920)
        scene.render.resolution_y = config.render.get("render_resolution_y", 1080)
        scene.render.engine = config.render.get("render_engine", "CYCLES")
        scene.cycles.samples = config.render.get("samples", 64)

    # Render
    bpy.ops.render.render(write_still=True)
