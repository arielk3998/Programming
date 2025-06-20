import bpy
from typing import Tuple, Optional


def add_donut(
    location: Tuple[float, float, float] = (0.0, 0.0, 3.0),
    major_radius: float = 1.0,
    minor_radius: float = 0.4,
    name: str = "Donut",
    rigid_body: bool = True,
    mass: float = 1.0,
    friction: float = 0.5,
    restitution: float = 0.7,
    smooth_shading: bool = True,
    subdivision_levels: int = 2,
    material_color: Tuple[float, float, float, float] = (0.9, 0.6, 0.3, 1.0),
    roughness: float = 0.4,
    subsurface: float = 0.2,
    material_name: str = "DonutMaterial"
) -> Optional[bpy.types.Object]:
    """
    Adds a torus ("donut") mesh to the scene with optional rigid body physics, smooth shading,
    subdivision surface modifier, and a customizable material.

    Args:
        location (tuple): The (x, y, z) location for the donut.
        major_radius (float): Major radius of the torus.
        minor_radius (float): Minor radius of the torus.
        name (str): Name to assign to the donut object.
        rigid_body (bool): Whether to add rigid body physics.
        mass (float): Rigid body mass.
        friction (float): Rigid body friction.
        restitution (float): Rigid body restitution (bounciness).
        smooth_shading (bool): Whether to apply smooth shading.
        subdivision_levels (int): Levels for the subdivision surface modifier.
        material_color (tuple): RGBA color for the material.
        roughness (float): Material roughness.
        subsurface (float): Material subsurface scattering.
        material_name (str): Name for the created material.

    Returns:
        bpy.types.Object or None: The created donut object, or None if creation failed.
    """
    try:
        bpy.ops.mesh.primitive_torus_add(
            major_radius=major_radius,
            minor_radius=minor_radius,
            location=location
        )
        donut = bpy.context.active_object
        donut.name = name

        if rigid_body:
            bpy.ops.rigidbody.object_add()
            donut.rigid_body.type = 'ACTIVE'
            donut.rigid_body.mass = mass
            donut.rigid_body.friction = friction
            donut.rigid_body.restitution = restitution

        if smooth_shading:
            bpy.ops.object.shade_smooth()

        subdiv = donut.modifiers.new(name="Subdivision", type='SUBSURF')
        subdiv.levels = subdivision_levels
        subdiv.render_levels = subdivision_levels

        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = material_color
            bsdf.inputs["Roughness"].default_value = roughness
            if "Subsurface" in bsdf.inputs:
                bsdf.inputs["Subsurface"].default_value = subsurface

        if len(donut.data.materials) == 0:
            donut.data.materials.append(mat)
        else:
            donut.data.materials[0] = mat

        return donut
    except Exception as e:
        print(f"Failed to add donut: {e}")
        return None
