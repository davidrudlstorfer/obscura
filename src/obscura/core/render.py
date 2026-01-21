"""Rendering utilities for the Obscura pipeline using Blender This module loads
a 3D mesh, applies user‑defined transformations, configures camera and lighting
automatically, assigns materials, and performs a final render using Blender."""

import math
import os

import bpy
import numpy as np
from munch import DefaultMunch


def render(config: DefaultMunch) -> None:
    """Rendering script for Obscura."""
    # --- Load parameters ---
    stl_path = config.paths.input_file
    output_path = config.paths.output_file

    # --- Start empty scene ---
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # --- Import STL mesh ---
    bpy.ops.wm.stl_import(filepath=stl_path)
    mesh_obj = bpy.context.selected_objects[0]

    # --- Apply basic transforms from params ---
    mesh_obj.scale = config.object_settings.get("mesh_scale", [1, 1, 1])
    mesh_obj.location = config.object_settings.get("mesh_location", [0, 0, 0])

    # --- Center origin ---
    bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS", center="BOUNDS")

    # --- Apply user-defined 3-axis rotation (in degrees) ---
    obj_rot_deg = config.object_settings.get("rotation", [0, 0, 0])
    mesh_obj.rotation_euler = [math.radians(a) for a in obj_rot_deg]

    # --- Compute bounding box and center ---
    bbox = np.asarray(mesh_obj.bound_box)
    center = bbox.mean(axis=0)
    max_extent = bbox.ptp(axis=0).max()

    # --- Automatic camera setup ---
    bpy.ops.object.camera_add(
        location=(center + [0, -2 * max_extent, max_extent]).tolist()
    )

    cam_obj = bpy.context.active_object
    cam_obj.data.lens = config.camera.get("camera_lens", 35)
    cam_obj.data.type = config.camera.get("camera_type", "PERSP")
    cam_obj.data.clip_end = max_extent * 10  # Ensure large/slender objects are visible

    # Track camera to object
    track = cam_obj.constraints.new("TRACK_TO")
    track.target = mesh_obj
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"
    bpy.context.scene.camera = cam_obj

    # --- Automatic lighting setup (simple SUNs) ---

    def setup_lighting(
        center: np.ndarray, max_extent: float, config: DefaultMunch
    ) -> tuple:
        """Set up three-point lighting using SUN lights."""

        # Key light
        bpy.ops.object.light_add(
            type="SUN",
            location=(center + [max_extent, -max_extent, max_extent]).tolist(),
        )
        key_light = bpy.context.active_object
        key_light.data.energy = config.light.get("key_light_intensity", 2.5)
        key_light.rotation_euler = (math.radians(-60), 0, math.radians(45))

        # Fill light
        bpy.ops.object.light_add(
            type="SUN",
            location=(center + [-max_extent, max_extent, max_extent]).tolist(),
        )

        fill_light = bpy.context.active_object
        fill_light.data.energy = config.light.get("fill_light_intensity", 1.5)
        fill_light.rotation_euler = (math.radians(-60), 0, math.radians(-45))

        # Back light
        bpy.ops.object.light_add(
            type="SUN", location=(center + [0, 0, 1.5 * max_extent]).tolist()
        )
        back_light = bpy.context.active_object
        back_light.data.energy = config.light.get("fill_light_intensity", 1.5) * 0.5
        back_light.rotation_euler = (math.radians(-30), 0, math.radians(180))

        return key_light, fill_light, back_light

    key_light, fill_light, back_light = setup_lighting(center, max_extent, config)

    # --- Material ---
    mat = bpy.data.materials.new(name="MeshMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = config.material.get(
            "material_color", [0.8, 0.2, 0.2, 1]
        )
        bsdf.inputs["Roughness"].default_value = config.material.get(
            "material_roughness", 0.5
        )
        bsdf.inputs["Metallic"].default_value = config.material.get(
            "material_metallic", 0.0
        )
    mesh_obj.data.materials.append(mat)

    # --- Ambient world ---
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new("World")
    bpy.context.scene.world.use_nodes = True
    bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = config.get(
            "background_color", [1, 1, 1, 1]
        )
        bg_node.inputs["Strength"].default_value = config.light.get(
            "ambient_light_strength", 0.2
        )

    # --- Render settings ---
    scene = bpy.context.scene
    scene.render.image_settings.file_format = "PNG"

    preview_mode = config.preview.get("preview_mode", False)  # Deactivated by default

    if preview_mode:
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

    # --- Render ---
    bpy.ops.render.render(write_still=True)
    print(f"Render saved to {scene.render.filepath}")
