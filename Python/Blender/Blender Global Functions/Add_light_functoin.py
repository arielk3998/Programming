import bpy
from typing import Tuple, Optional

def add_light(
    light_type: str = 'AREA',
    location: Tuple[float, float, float] = (4.0, -4.0, 6.0),
    energy: float = 1000.0,
    size: float = 5.0,
    name: str = "AreaLight",
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
) -> Optional[bpy.types.Object]:
    """
    Adds a light to the scene with customizable parameters.

    Args:
        light_type (str): Type of the light ('POINT', 'SUN', 'SPOT', 'AREA').
        location (tuple): (x, y, z) location for the light.
        energy (float): Light energy (intensity).
        size (float): Size of the light (for area and spot lights).
        name (str): Name to assign to the light object.
        color (tuple): RGB color of the light.

    Returns:
        bpy.types.Object or None: The created light object, or None if creation failed.
    """
    try:
        bpy.ops.object.light_add(type=light_type, location=location)
        light = bpy.context.active_object
        light.name = name
        light.data.energy = energy
        light.data.color = color
        if hasattr(light.data, "size"):
            light.data.size = size
        return light
    except Exception as e:
        print(f"Failed to add light: {e}")
        return None

