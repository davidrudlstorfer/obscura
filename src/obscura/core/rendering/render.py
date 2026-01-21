"""Rendering pipeline.

This module loads a 3D mesh, applies user‑defined transformations,
configures camera and lighting automatically, assigns materials, and
performs a final render using Blender.
"""

import bpy
from munch import DefaultMunch

from .background import define_background
from .camera import setup_camera
from .lighting import ambient_lighting, setup_lighting
from .material import apply_material
from .object_settings import apply_transforms, compute_geometry, load_mesh
from .render_settings import configure_render


def render(config: DefaultMunch) -> None:
    """Rendering script for Obscura."""

    # --- Start empty scene ---
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # --- Object loading and transformation from object_settings.py ---
    mesh_obj = load_mesh(config)  # Import STL mesh
    apply_transforms(mesh_obj, config)
    center, max_extent = compute_geometry(mesh_obj)

    # --- Camera set-up from camera.py ---
    cam = setup_camera(config, mesh_obj, center, max_extent)

    # --- Ambient world from background.py and lighting.py---
    define_background(config)
    ambient_lighting(config)

    # --- Automatic lighting setup (simple SUNs) from lighting.py ---
    key_light, fill_light, back_light = setup_lighting(center, max_extent, config)

    # --- Apply defined material properties from material.py ---
    apply_material(mesh_obj, config)

    # --- Render settings ---
    scene = bpy.context.scene
    configure_render(scene, config)

    print(f"Render saved to {scene.render.filepath}")
