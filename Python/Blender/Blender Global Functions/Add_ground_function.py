import bpy
from typing import Tuple, Optional

def add_ground(
    size: float = 8.0,
    location: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    name: str = "Ground",
    friction: float = 0.5,
    restitution: float = 0.7,
    rigid_body: bool = True
) -> Optional[bpy.types.Object]:
    """
    Adds a ground plane to the scene with optional rigid body physics.

    Args:
        size (float): Size of the ground plane.
        location (tuple): (x, y, z) location for the ground plane.
        name (str): Name to assign to the ground object.
        friction (float): Rigid body friction.
        restitution (float): Rigid body restitution (bounciness).
        rigid_body (bool): Whether to add rigid body physics.

    Returns:
        bpy.types.Object or None: The created ground object, or None if creation failed.
    """
    try:
        bpy.ops.mesh.primitive_plane_add(size=size, location=location)
        ground = bpy.context.active_object
        ground.name = name

        if rigid_body:
            bpy.ops.rigidbody.object_add()
            ground.rigid_body.type = 'PASSIVE'
            ground.rigid_body.friction = friction
            ground.rigid_body.restitution = restitution

        return ground
    except Exception as e:
        print(f"Failed to add ground: {e}")
        return None