import bpy

def bake_physics(
    steps_per_second: int = 120,
    solver_iterations: int = 25,
    verbose: bool = True
) -> bool:
    """
    Bake the physics simulation for all objects in the current scene.

    Args:
        steps_per_second (int): Number of simulation steps per second.
        solver_iterations (int): Number of solver iterations for the simulation.
        verbose (bool): Whether to print status messages.

    Returns:
        bool: True if baking succeeded, False otherwise.
    """
    try:
        if not bpy.context.scene.rigidbody_world:
            bpy.ops.rigidbody.world_add()
            if verbose:
                print("Rigidbody world added to the scene.")

        rbw = bpy.context.scene.rigidbody_world
        if hasattr(rbw, "steps_per_second"):
            rbw.steps_per_second = steps_per_second
        if hasattr(rbw, "solver_iterations"):
            rbw.solver_iterations = solver_iterations

        bpy.ops.ptcache.bake_all(bake=True)
        if verbose:
            print("Physics baking completed successfully.")
        return True
    except Exception as e:
        if verbose:
            print(f"Physics baking failed: {e}")
        return False