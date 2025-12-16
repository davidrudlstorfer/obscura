"""Parametric rendering script for Blender."""

import json
import math
import os
import sys

import bpy
import numpy as np

if __name__ == "__main__":
    # --- Parse command line arguments ---
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
    else:
        argv = []

    preview_mode = "--preview" in argv
    if preview_mode:
        argv.remove("--preview")

    params_file = argv[0] if len(argv) > 0 else "/workspace/output/params.json"

    # --- Load parameters ---
    with open(params_file, "r") as f:
        params = json.load(f)

    stl_path = params["input_file"]
    output_path = params["output_file"]

    # --- Start empty scene ---
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # --- Import STL mesh ---
    bpy.ops.wm.stl_import(filepath=stl_path)
    mesh_obj = bpy.context.selected_objects[0]

    # --- Apply basic transforms from params ---
    mesh_obj.scale = params.get("mesh_scale", [1, 1, 1])
    mesh_obj.location = params.get("mesh_location", [0, 0, 0])

    # --- Center origin ---
    bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS", center="BOUNDS")

    # --- Apply user-defined 3-axis rotation (in degrees) ---
    obj_rot_deg = params.get("object_rotation", [0, 0, 0])
    mesh_obj.rotation_euler = [math.radians(a) for a in obj_rot_deg]

    # --- Compute bounding box and center ---
    bbox = np.array(mesh_obj.bound_box)
    min_corner = bbox.min(axis=0)
    max_corner = bbox.max(axis=0)
    center = (min_corner + max_corner) / 2
    dims = max_corner - min_corner
    max_dim = max(dims)

    # --- Automatic camera setup ---
    cam_location = center + np.array([0, -max_dim * 2, max_dim])
    bpy.ops.object.camera_add(location=cam_location.tolist())

    cam_obj = bpy.context.active_object
    cam_obj.data.lens = params.get("camera_lens", 35)
    cam_obj.data.type = params.get("camera_type", "PERSP")
    cam_obj.data.clip_end = max_dim * 10  # Ensure large/slender objects are visible

    # Track camera to object
    track = cam_obj.constraints.new("TRACK_TO")
    track.target = mesh_obj
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"
    bpy.context.scene.camera = cam_obj

    # --- Automatic lighting setup (simple SUNs) ---

    def setup_lighting(center: np.ndarray, max_dim: float, params: dict) -> tuple:
        """Set up three-point lighting using SUN lights."""

        # Key light
        bpy.ops.object.light_add(
            type="SUN",
            location=(center + np.array([max_dim, -max_dim, max_dim])).tolist(),
        )
        key_light = bpy.context.active_object
        key_light.data.energy = params.get("key_light_intensity", 2.5)
        key_light.rotation_euler = (math.radians(-60), 0, math.radians(45))

        # Fill light
        bpy.ops.object.light_add(
            type="SUN",
            location=(center + np.array([-max_dim, max_dim, max_dim])).tolist(),
        )

        fill_light = bpy.context.active_object
        fill_light.data.energy = params.get("fill_light_intensity", 1.5)
        fill_light.rotation_euler = (math.radians(-60), 0, math.radians(-45))

        # Back light
        bpy.ops.object.light_add(
            type="SUN", location=(center + np.array([0, 0, max_dim * 1.5])).tolist()
        )
        back_light = bpy.context.active_object
        back_light.data.energy = params.get("fill_light_intensity", 1.5) * 0.5
        back_light.rotation_euler = (math.radians(-30), 0, math.radians(180))

        return key_light, fill_light, back_light

    key_light, fill_light, back_light = setup_lighting(center, max_dim, params)

    # --- Material ---
    mat = bpy.data.materials.new(name="MeshMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = params.get(
            "material_color", [0.8, 0.2, 0.2, 1]
        )
        bsdf.inputs["Roughness"].default_value = params.get("material_roughness", 0.5)
        bsdf.inputs["Metallic"].default_value = params.get("material_metallic", 0.0)
    mesh_obj.data.materials.append(mat)

    # --- Ambient world ---
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new("World")
    bpy.context.scene.world.use_nodes = True
    bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = params.get(
            "background_color", [1, 1, 1, 1]
        )
        bg_node.inputs["Strength"].default_value = params.get(
            "ambient_light_strength", 0.2
        )

    # --- Render settings ---
    scene = bpy.context.scene
    scene.render.image_settings.file_format = "PNG"

    if preview_mode:
        base, ext = os.path.splitext(output_path)
        scene.render.filepath = f"{base}_preview{ext}"
        scene.render.resolution_x = params.get("preview_resolution_x", 640)
        scene.render.resolution_y = params.get("preview_resolution_y", 360)
        scene.render.engine = params.get("preview_engine", "BLENDER_EEVEE_NEXT")
        if scene.render.engine == "CYCLES":
            scene.cycles.samples = params.get("preview_samples", 8)
            scene.cycles.use_denoising = params.get("preview_use_denoising", True)
    else:
        scene.render.filepath = output_path
        scene.render.resolution_x = params.get("render_resolution_x", 1920)
        scene.render.resolution_y = params.get("render_resolution_y", 1080)
        scene.render.engine = params.get("render_engine", "CYCLES")
        scene.cycles.samples = params.get("samples", 64)

    # --- Render ---
    bpy.ops.render.render(write_still=True)
    print(f"Render saved to {scene.render.filepath}")
