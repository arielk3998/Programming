import bpy
import math
from typing import Tuple, Optional

def add_camera(
    location: Tuple[float, float, float] = (5.0, -5.0, 5.0),
    rotation: Tuple[float, float, float] = (math.radians(60), 0.0, math.radians(45)),
    focus_distance: float = 5.0,
    aperture_fstop: float = 2.8,
    use_dof: bool = True,
    set_scene_camera: bool = True,
    camera_name: Optional[str] = None
) -> Optional[bpy.types.Object]:
    """
    Adds a camera to the scene with optional depth of field settings.

    Args:
        location (tuple): The (x, y, z) location for the camera.
        rotation (tuple): The (x, y, z) Euler rotation in radians.
        focus_distance (float): Depth of field focus distance.
        aperture_fstop (float): Aperture f-stop for depth of field.
        use_dof (bool): Whether to enable depth of field.
        set_scene_camera (bool): Whether to set this camera as the active scene camera.
        camera_name (str, optional): Name to assign to the camera object.

    Returns:
        bpy.types.Object or None: The created camera object, or None if creation failed.
    """
    # 1. Check if bpy is available
    if bpy is None:
        print("bpy module not available. This function must be run inside Blender.")
        return None

    # 2. Validate location and rotation types
    if not (isinstance(location, tuple) and len(location) == 3 and all(isinstance(x, (int, float)) for x in location)):
        print("Invalid location. Must be a tuple of 3 numbers.")
        return None
    if not (isinstance(rotation, tuple) and len(rotation) == 3 and all(isinstance(x, (int, float)) for x in rotation)):
        print("Invalid rotation. Must be a tuple of 3 numbers.")
        return None

    # 3. Validate focus_distance and aperture_fstop
    if not isinstance(focus_distance, (int, float)) or focus_distance <= 0:
        print("Invalid focus_distance. Must be a positive number.")
        return None
    if not isinstance(aperture_fstop, (int, float)) or aperture_fstop <= 0:
        print("Invalid aperture_fstop. Must be a positive number.")
        return None

    # 4. Validate use_dof and set_scene_camera
    if not isinstance(use_dof, bool):
        print("use_dof must be a boolean.")
        return None
    if not isinstance(set_scene_camera, bool):
        print("set_scene_camera must be a boolean.")
        return None

    # 5. Validate camera_name
    if camera_name is not None and not isinstance(camera_name, str):
        print("camera_name must be a string or None.")
        return None

    try:
        # 6. Deselect all objects before adding
        bpy.ops.object.select_all(action='DESELECT')

        # 7. Add camera
        bpy.ops.object.camera_add(location=location, rotation=rotation)
        camera = bpy.context.active_object

        # 8. Check if camera was created
        if camera is None or camera.type != 'CAMERA':
            print("Camera creation failed: No active camera object after camera_add.")
            return None

        # 9. Assign name
        camera.name = camera_name if camera_name else "Camera"

        # 10. Set as scene camera if requested
        if set_scene_camera:
            bpy.context.scene.camera = camera

        # 11. Access camera data safely
        camera_data = getattr(camera, "data", None)
        if camera_data is None or camera_data.type != 'CAMERA':
            print("Camera data not found or not of type CAMERA.")
            return None

        # 12. Set depth of field
        if hasattr(camera_data, "dof"):
            camera_data.dof.use_dof = use_dof
            if use_dof:
                camera_data.dof.focus_distance = focus_distance
                camera_data.dof.aperture_fstop = aperture_fstop
        else:
            print("Camera data does not support depth of field.")

        # 13. Move camera to a new collection if needed (optional, for organization)
        # collection = bpy.context.scene.collection
        # if camera.name not in collection.objects:
        #     collection.objects.link(camera)

        # 14. Ensure camera is visible and selectable
        camera.hide_viewport = False
        camera.hide_render = False
        camera.hide_set(False)
        camera.select_set(True)

        # 15. Set camera as active object
        bpy.context.view_layer.objects.active = camera

        # 16. Return the camera object
        return camera

    except Exception as e:
        print(f"Failed to add camera: {e}")
        return None

