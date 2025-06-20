try:
    import bpy # type: ignore
except ImportError:
    bpy = None  # Allows code completion in editors, but only works in Blender

def clear_scene(verbose: bool = True, remove_orphans: bool = True, reset_cursor: bool = True) -> None:
    """
    Deletes all objects in the current Blender scene and optionally removes orphan data.

    Args:
        verbose (bool): Whether to print status messages.
        remove_orphans (bool): Whether to remove orphan data blocks (meshes, materials, etc.).
        reset_cursor (bool): Whether to reset the 3D cursor and frame to defaults.
    """
    if bpy is None:
        if verbose:
            print("bpy module not available. This function must be run inside Blender.")
        return

    try:
        # Deselect all, select all, and delete
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        if verbose:
            print("All objects deleted from the scene.")

        # Remove orphan data blocks for a truly clean scene
        if remove_orphans:
            for _ in range(3):  # Run multiple times to ensure all are purged
                bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
            if verbose:
                print("Orphan data blocks purged.")

        # Reset 3D cursor and frame
        if reset_cursor:
            bpy.context.scene.frame_set(1)
            bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
            if verbose:
                print("3D cursor and frame reset.")

    except Exception as e:
        if verbose:
            print(f"Scene clearing failed: {e}")

if __name__ == "__main__":
    clear_scene()