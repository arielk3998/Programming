"""
================================================================================
Blender Donut Anime-Style Camera Animation Utilities
================================================================================

This script provides functions to add a camera to your Blender scene and animate
it in a dramatic, anime-inspired fashion—flying through the hole of a donut with
slow-motion and a rolling camera effect.

SCENE OVERVIEW:
---------------
- The camera is placed and configured with depth of field for cinematic focus.
- A Bezier curve path is generated to guide the camera through the donut hole.
- The camera is animated to follow this path, with slow-motion in the middle.
- The camera spins (rolls) as it flies through the donut for extra anime flair.

FUNCTIONS:
----------

1. add_camera(...)
   - Adds a camera to the scene at a specified location and rotation.
   - Configures depth of field (DOF) for realistic focus blur.
   - Optionally sets this camera as the active scene camera.
   - Returns the created camera object.

2. animate_camera_fly_through(...)
   - Creates a curved path through the donut hole.
   - Animates the camera to follow this path, flying through the donut.
   - Adds slow-motion by adjusting animation keyframes.
   - Adds dramatic camera roll for an anime-style effect.

USAGE EXAMPLE:
--------------
    donut = add_donut()  # Your donut creation function
    camera = add_camera()
    animate_camera_fly_through(camera, donut)

TIPS:
-----
- Adjust the 'frames' and 'slowmo_factor' parameters for different speeds.
- Enable motion blur and DOF in Blender's render settings for best results.
- Render the animation to see the full effect!

================================================================================
"""

import bpy # type: ignore
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

def animate_camera_fly_through(
    camera_obj,
    donut_obj,
    frames: int = 120,
    slowmo_factor: float = 2.0
):
    """
    Animates the camera flying through the donut hole with slow-motion and dramatic rotation.
    Args:
        camera_obj: The camera object to animate.
        donut_obj: The donut object to fly through.
        frames: Total frames for the animation.
        slowmo_factor: How much to slow down in the middle (higher = slower).
    """
    # 1. Create a path (Bezier curve) through the donut hole
    bpy.ops.curve.primitive_bezier_curve_add()
    path = bpy.context.active_object
    path.name = "DonutFlyThroughPath"
    curve = path.data

    # 2. Position curve points: start outside, pass through center, exit behind
    major_radius = donut_obj.dimensions.x / 2
    minor_radius = donut_obj.dimensions.z / 2
    donut_center = donut_obj.location

    # Set curve points
    curve.splines[0].bezier_points[0].co = (donut_center.x - major_radius * 2, donut_center.y, donut_center.z)
    curve.splines[0].bezier_points[1].co = (donut_center.x + major_radius * 2, donut_center.y, donut_center.z)
    # Add a middle point at the donut center for dramatic effect
    mid_point = curve.splines[0].bezier_points[0].handle_right
    curve.splines[0].bezier_points[0].handle_right_type = 'FREE'
    curve.splines[0].bezier_points[1].handle_left_type = 'FREE'

    # 3. Add a Follow Path constraint to the camera
    camera_obj.constraints.clear()
    follow = camera_obj.constraints.new(type='FOLLOW_PATH')
    follow.target = path
    follow.use_curve_follow = True

    # 4. Animate camera along the path
    path.data.path_duration = frames
    bpy.context.view_layer.objects.active = path
    bpy.ops.object.select_all(action='DESELECT')
    path.select_set(True)
    bpy.context.view_layer.objects.active = path

    # Insert keyframes for evaluation time (controls camera position on path)
    path.data.use_path = True
    path.data.eval_time = 0
    path.data.keyframe_insert(data_path="eval_time", frame=1)
    path.data.eval_time = frames
    path.data.keyframe_insert(data_path="eval_time", frame=frames)

    # 5. Slow-motion effect: adjust F-curve interpolation
    fcurve = path.data.animation_data.action.fcurves.find('eval_time')
    if fcurve:
        for kp in fcurve.keyframe_points:
            kp.interpolation = 'EASE_IN_OUT'
        # Add slowmo in the middle by manipulating handles
        mid_frame = frames // 2
        fcurve.keyframe_points.insert(frame=mid_frame, value=frames // slowmo_factor, options={'FAST'})
        fcurve.update()

    # 6. Add dramatic camera roll (anime style)
    camera_obj.rotation_mode = 'XYZ'
    camera_obj.keyframe_insert(data_path="rotation_euler", frame=1)
    camera_obj.rotation_euler[1] = math.radians(0)  # No tilt at start
    camera_obj.keyframe_insert(data_path="rotation_euler", frame=mid_frame)
    camera_obj.rotation_euler[1] = math.radians(360)  # Full roll at mid
    camera_obj.keyframe_insert(data_path="rotation_euler", frame=frames)
    
    print("Camera fly-through animation created! Render your animation to see the effect.")

# Example usage after creating donut and camera:
# donut = add_donut()
# camera = add_camera()
# animate_camera_fly_through(camera, donut)

