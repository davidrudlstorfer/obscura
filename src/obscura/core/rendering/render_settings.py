"""Rendering settings and final image generation in Blender."""

import logging
import os
from typing import Any

import bpy

log = logging.getLogger("obscura")


def _configure_render_device(scene: bpy.types.Scene) -> None:
    """Enable GPU rendering for Cycles if a compatible device is available,
    else fall back to CPU."""
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.get_devices()  # refresh the list of detected devices

    # Prefer OptiX (uses RT cores, faster on Ada/RTX cards) over plain CUDA
    device_type = next(
        (t for t in ("OPTIX", "CUDA") if any(d.type == t for d in prefs.devices)),
        None,
    )

    if device_type is None:
        scene.cycles.device = "CPU"
        log.info("No compatible GPU detected - rendering on CPU.")
        return

    prefs.compute_device_type = device_type
    scene.cycles.device = "GPU"
    for d in prefs.devices:
        d.use = d.type == device_type

    log.info(f"GPU detected - rendering on {device_type}.")


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
            _configure_render_device(scene)
        # Eevee Next has no configurable preview effects

    else:
        scene.render.filepath = output_path
        scene.render.resolution_x = config.render.resolution_x
        scene.render.resolution_y = config.render.resolution_y
        scene.render.engine = config.render.engine
        if scene.render.engine == "CYCLES":
            scene.cycles.samples = config.render.samples
            scene.cycles.use_denoising = True
            _configure_render_device(scene)

    # Render
    bpy.ops.render.render(write_still=True)
