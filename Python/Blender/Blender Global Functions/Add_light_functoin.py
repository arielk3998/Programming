import bpy # type: ignore
from typing import Tuple, Optional

def add_light(
    light_type: str = 'AREA',
    location: Tuple[float, float, float] = (4.0, -4.0, 6.0),
    energy: float = 1000.0,
    size: float = 5.0,
    name: str = "AreaLight",
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    spot_angle: float = 1.0472  # 60 degrees in radians
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
        spot_angle (float): Angle for spot lights (in radians).

    Returns:
        bpy.types.Object or None: The created light object, or None if creation failed.
    """
    try:
        valid_types = {'POINT', 'SUN', 'SPOT', 'AREA'}
        if light_type not in valid_types:
            raise ValueError(f"Invalid light_type '{light_type}'. Must be one of {valid_types}.")

        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.light_add(type=light_type, location=location)
        light = bpy.context.active_object
        light.name = name
        light.data.energy = energy
        light.data.color = color

        # Set size for supported types
        if hasattr(light.data, "size"):
            light.data.size = size
        if light_type == 'SPOT':
            light.data.spot_size = spot_angle
        if light_type == 'SUN' and hasattr(light.data, "angle"):
            light.data.angle = 0.1  # Sun softness

        print(f"Light '{name}' of type '{light_type}' created at {location} with energy {energy}.")
        return light
    except Exception as e:
        print(f"Failed to add light: {e}")
        return None

