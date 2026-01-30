"""Material utilities for Blender."""

from typing import Any

import bpy


def apply_material(mesh_obj: bpy.types.Object, config: Any) -> None:
    """Create and apply a material to the mesh."""
    mat = bpy.data.materials.new(name="MeshMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = config.material.material_color
        bsdf.inputs["Roughness"].default_value = config.material.material_roughness
        bsdf.inputs["Metallic"].default_value = config.material.material_metallic

    mesh_obj.data.materials.append(mat)
