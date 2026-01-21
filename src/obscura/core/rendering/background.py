"""Rendering background for Blender."""

import bpy
from munch import DefaultMunch


def define_background(config: DefaultMunch) -> None:
    """Configure the world background color for the scene."""
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new("World")
    bpy.context.scene.world.use_nodes = True
    bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = config.get(
            "background_color", [1, 1, 1, 1]
        )
