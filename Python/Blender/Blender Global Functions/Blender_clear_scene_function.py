try:
    import bpy
except ImportError:
    bpy = None  # Allows code completion in editors, but only works in Blender

def clear_scene(verbose: bool = True) -> None:
    """
    Deletes all objects in the current Blender scene.

    Args:
        verbose (bool): Whether to print status messages.
    """
    if bpy is None:
        if verbose:
            print("bpy module not available. This function must be run inside Blender.")
        return

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    if verbose:
        print("All objects deleted from the scene.")

if __name__ == "__main__":
    clear_scene()