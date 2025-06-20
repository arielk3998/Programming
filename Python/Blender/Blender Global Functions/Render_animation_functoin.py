import bpy # type: ignore
import os

def render_animation(
    frame_start: int = 1,
    frame_end: int = 100,
    output_path: str = "//render/",
    file_format: str = "FFMPEG",
    verbose: bool = True
) -> None:
    """
    Renders the animation for the current scene.

    Args:
        frame_start (int): The first frame to render.
        frame_end (int): The last frame to render.
        output_path (str): The directory to save rendered frames or video.
        file_format (str): Output file format ('FFMPEG', 'AVI_JPEG', etc.).
        verbose (bool): Whether to print status messages.
    """
    try:
        scene = bpy.context.scene

        # Ensure output directory exists (if not using Blender's // relative path)
        if not output_path.startswith("//"):
            os.makedirs(bpy.path.abspath(output_path), exist_ok=True)

        # Store previous settings to restore after rendering
        prev_frame_start = scene.frame_start
        prev_frame_end = scene.frame_end
        prev_filepath = scene.render.filepath
        prev_format = scene.render.image_settings.file_format

        # Set render settings
        scene.frame_start = frame_start
        scene.frame_end = frame_end
        scene.render.filepath = output_path
        scene.render.image_settings.file_format = file_format

        if verbose:
            print(f"Rendering animation from frame {frame_start} to {frame_end} to '{output_path}' as {file_format}.")

        bpy.ops.render.render(animation=True)

        if verbose:
            print("Animation rendering completed.")

        # Restore previous settings
        scene.frame_start = prev_frame_start
        scene.frame_end = prev_frame_end
        scene.render.filepath = prev_filepath
        scene.render.image_settings.file_format = prev_format

    except Exception as e:
        if verbose:
            print(f"Animation rendering failed: {e}")

if __name__ == "__main__":
    render_animation()