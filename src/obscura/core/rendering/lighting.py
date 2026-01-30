"""Lighting utilities for Blender."""

import math
from typing import Any

import bpy
import numpy as np


def setup_lighting(center: np.ndarray, max_extent: float, config: Any) -> None:
    """Set up three-point lighting using SUN lights."""

    # Key light
    bpy.ops.object.light_add(
        type="SUN",
        location=(center + [max_extent, -max_extent, max_extent]).tolist(),
    )
    key_light = bpy.context.active_object
    key_light.data.energy = config.light.key_light_intensity
    key_light.rotation_euler = (math.radians(-60), 0, math.radians(45))

    # Fill light
    bpy.ops.object.light_add(
        type="SUN",
        location=(center + [-max_extent, max_extent, max_extent]).tolist(),
    )

    fill_light = bpy.context.active_object
    fill_light.data.energy = config.light.fill_light_intensity
    fill_light.rotation_euler = (math.radians(-60), 0, math.radians(-45))

    # Back light
    bpy.ops.object.light_add(
        type="SUN", location=(center + [0, 0, 1.5 * max_extent]).tolist()
    )
    back_light = bpy.context.active_object
    back_light.data.energy = (
        config.light.fill_light_intensity * 0.5
    )  # intentionally set weaker than the fill light (classic 3‑point lighting ratio)
    back_light.rotation_euler = (math.radians(-30), 0, math.radians(180))


def ambient_lighting(config: Any) -> None:
    """Configure ambient world lighting."""
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new("World")

    bpy.context.scene.world.use_nodes = True
    bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = config.background_color
