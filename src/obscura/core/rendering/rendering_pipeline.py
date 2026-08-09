"""Rendering pipeline.

This module loads a 3D mesh, applies user‑defined transformations,
configures camera and lighting automatically, assigns materials, and
performs a final render using Blender.
"""

import logging
import os
from typing import Any

import bpy

from obscura.core.rendering.background import define_background
from obscura.core.rendering.camera import setup_camera
from obscura.core.rendering.lighting import ambient_lighting, setup_lighting
from obscura.core.rendering.material import apply_material
from obscura.core.rendering.object_settings import (
    apply_transforms,
    compute_geometry,
    load_mesh,
)
from obscura.core.rendering.render_settings import render

log = logging.getLogger("obscura")


def rendering_pipeline(config: Any) -> None:
    """Rendering script for Obscura."""
    input_file_path = config.general.input_file_path

    if os.path.splitext(input_file_path)[1].lower() == ".blend":
        bpy.ops.wm.open_mainfile(filepath=input_file_path)
    else:
        # Start empty scene
        bpy.ops.wm.read_factory_settings(use_empty=True)

        # Object loading and transformation from object_settings.py
        mesh_obj = load_mesh(config)
        apply_transforms(mesh_obj, config)
        center, max_extent = compute_geometry(mesh_obj)

        # Camera set-up from camera.py
        setup_camera(config, mesh_obj, center, max_extent)

        # Ambient world from background.py
        define_background(config)
        ambient_lighting(config)

        # Automatic lighting setup (simple SUNs) from lighting.py
        setup_lighting(center, max_extent, config)

        # Apply defined material properties from material.py
        apply_material(mesh_obj, config)

    # Render settings & execution
    scene = bpy.context.scene
    render(scene, config)

    log.info("Render saved to " + str(scene.render.filepath))
