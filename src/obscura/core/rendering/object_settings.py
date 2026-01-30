"""Object loading, applying transforms, and computing object geometry in
Blender."""

import math
from typing import Any

import bpy
import numpy as np


def load_mesh(config: Any) -> bpy.types.Object:
    """Import the STL mesh and return the Blender object."""
    stl_path = config.paths.input_file
    bpy.ops.wm.stl_import(filepath=stl_path)
    return bpy.context.selected_objects[0]


def apply_transforms(mesh_obj: bpy.types.Object, config: Any) -> None:
    """Apply basic transforms from params (scale, location, and rotation)"""
    mesh_obj.scale = config.object_settings.mesh_scale
    mesh_obj.location = config.object_settings.mesh_location

    bpy.ops.object.origin_set(
        type="ORIGIN_CENTER_OF_MASS", center="BOUNDS"
    )  # Center origin

    obj_rot_deg = (
        config.object_settings.rotation
    )  # Apply user-defined 3-axis rotation (in degrees)
    mesh_obj.rotation_euler = [math.radians(a) for a in obj_rot_deg]


def compute_geometry(mesh_obj: bpy.types.Object) -> tuple[np.ndarray, float]:
    """Compute bounding box center and maximum extent."""
    bbox = np.asarray(mesh_obj.bound_box)
    center = bbox.mean(axis=0)
    max_extent = bbox.ptp(axis=0).max()
    return center, max_extent
