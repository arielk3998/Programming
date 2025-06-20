import bpy # type: ignore
from typing import Tuple, Optional

def add_ground(
    size: float = 8.0,
    location: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    name: str = "Ground",
    friction: float = 0.5,
    restitution: float = 0.7,
    rigid_body: bool = True,
    use_material: bool = True,
    material_name: str = "GroundMaterial"
) -> Optional[bpy.types.Object]:
    """
    Adds a ground plane to the scene with optional rigid body physics and a procedural material.

    Args:
        size (float): Size of the ground plane.
        location (tuple): (x, y, z) location for the ground plane.
        name (str): Name to assign to the ground object.
        friction (float): Rigid body friction.
        restitution (float): Rigid body restitution (bounciness).
        rigid_body (bool): Whether to add rigid body physics.
        use_material (bool): Whether to add a procedural material to the ground.
        material_name (str): Name for the ground material.

    Returns:
        bpy.types.Object or None: The created ground object, or None if creation failed.
    """
    try:
        # Deselect all and add the plane
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.mesh.primitive_plane_add(size=size, location=location)
        ground = bpy.context.active_object
        ground.name = name

        # Add rigid body physics if requested
        if rigid_body:
            bpy.ops.rigidbody.object_add()
            ground.rigid_body.type = 'PASSIVE'
            ground.rigid_body.friction = friction
            ground.rigid_body.restitution = restitution

        # Add a procedural material for realism
        if use_material:
            mat = bpy.data.materials.new(name=material_name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            nodes.clear()

            output = nodes.new("ShaderNodeOutputMaterial")
            bsdf = nodes.new("ShaderNodeBsdfPrincipled")
            noise = nodes.new("ShaderNodeTexNoise")
            bump = nodes.new("ShaderNodeBump")
            mapping = nodes.new("ShaderNodeMapping")
            texcoord = nodes.new("ShaderNodeTexCoord")
            colorramp = nodes.new("ShaderNodeValToRGB")

            # Color ramp for subtle variation (gray to brownish)
            colorramp.color_ramp.elements[0].color = (0.7, 0.7, 0.7, 1)
            colorramp.color_ramp.elements[1].color = (0.4, 0.3, 0.2, 1)

            links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
            links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
            noise.inputs['Scale'].default_value = 3.0
            links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
            links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
            links.new(noise.outputs['Fac'], bump.inputs['Height'])
            bump.inputs['Strength'].default_value = 0.15
            links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
            bsdf.inputs['Roughness'].default_value = 0.7
            links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

            ground.data.materials.clear()
            ground.data.materials.append(mat)

        print(f"Ground plane '{name}' created at {location} with size {size}.")
        return ground
    except Exception as e:
        print(f"Failed to add ground: {e}")
        return None