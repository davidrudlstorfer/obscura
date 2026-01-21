"""Lighting utilities for Blender."""

import math

import bpy
import numpy as np
from munch import DefaultMunch


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


def ambient_lighting(config: DefaultMunch) -> None:
    """Configure ambient world lighting."""
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new("World")

    bpy.context.scene.world.use_nodes = True
    bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = config.get(
            "background_color", [1, 1, 1, 1]
        )
