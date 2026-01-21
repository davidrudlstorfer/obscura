"""Camera utilities for Blender."""

import bpy
import numpy as np
from munch import DefaultMunch


def setup_camera(
    config: DefaultMunch,
    mesh_obj: bpy.types.Object,
    center: np.ndarray,
    max_extent: float,
) -> bpy.types.Object:
    """Create and configure camera settings."""

    bpy.ops.object.camera_add(  # Automatic camera setup
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

    return cam_obj
