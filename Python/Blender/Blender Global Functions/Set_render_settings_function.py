import bpy
import os

def set_render_settings(
    output_path: str,
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    fps: int = 30,
    file_format: str = 'FFMPEG',
    verbose: bool = True
) -> None:
    """
    Sets render resolution, frame rate, file format, and output path for the current Blender scene.

    Args:
        output_path (str): The file path for rendered output.
        resolution_x (int): Horizontal resolution in pixels.
        resolution_y (int): Vertical resolution in pixels.
        fps (int): Frames per second.
        file_format (str): Output file format (e.g., 'FFMPEG', 'AVI_JPEG').
        verbose (bool): Whether to print status messages.
    """
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        if verbose:
            print(f"Created output directory: {output_dir}")

    scene = bpy.context.scene
    scene.render.filepath = output_path
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.fps = fps
    scene.render.image_settings.file_format = file_format

    if verbose:
        print(f"Render settings applied: {resolution_x}x{resolution_y} @ {fps}fps, format={file_format}, output='{output_path}'")

