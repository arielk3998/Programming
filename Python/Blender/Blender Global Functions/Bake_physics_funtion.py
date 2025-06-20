import bpy # type: ignore

def bake_physics(
    steps_per_second: int = 120,
    solver_iterations: int = 25,
    verbose: bool = True,
    clear_cache: bool = True,
    frame_start: int = None,
    frame_end: int = None
) -> bool:
    """
    Bake the physics simulation for all objects in the current scene.

    Args:
        steps_per_second (int): Number of simulation steps per second.
        solver_iterations (int): Number of solver iterations for the simulation.
        verbose (bool): Whether to print status messages.
        clear_cache (bool): Whether to clear previous bakes before baking.
        frame_start (int, optional): Start frame for baking. Defaults to scene start.
        frame_end (int, optional): End frame for baking. Defaults to scene end.

    Returns:
        bool: True if baking succeeded, False otherwise.
    """
    try:
        scene = bpy.context.scene
        if not scene.rigidbody_world:
            bpy.ops.rigidbody.world_add()
            if verbose:
                print("Rigidbody world added to the scene.")

        rbw = scene.rigidbody_world
        if hasattr(rbw, "steps_per_second"):
            rbw.steps_per_second = steps_per_second
        if hasattr(rbw, "solver_iterations"):
            rbw.solver_iterations = solver_iterations

        # Set frame range if specified
        if frame_start is not None:
            scene.frame_start = frame_start
        if frame_end is not None:
            scene.frame_end = frame_end

        if clear_cache:
            bpy.ops.ptcache.free_bake_all()
            if verbose:
                print("Cleared previous physics bakes.")

        bpy.ops.ptcache.bake_all(bake=True)
        if verbose:
            obj_count = sum(1 for obj in scene.objects if obj.rigid_body)
            print(f"Physics baking completed successfully for {obj_count} rigid body object(s).")
        return True
    except Exception as e:
        if verbose:
            print(f"Physics baking failed: {e}")
        return False