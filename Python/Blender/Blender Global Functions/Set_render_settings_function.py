import bpy # type: ignore
import os

def set_render_settings(
    output_path: str,
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    fps: int = 30,
    file_format: str = 'FFMPEG',
    ffmpeg_codec: str = 'H264',
    ffmpeg_format: str = 'MPEG4',
    color_mode: str = 'RGB',
    color_depth: str = '8',
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
        ffmpeg_codec (str): Codec for FFMPEG output (e.g., 'H264').
        ffmpeg_format (str): Container format for FFMPEG (e.g., 'MPEG4').
        color_mode (str): Color mode ('RGB', 'BW', 'RGBA').
        color_depth (str): Color depth ('8', '16').
        verbose (bool): Whether to print status messages.
    """
    try:
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
        scene.render.image_settings.color_mode = color_mode
        scene.render.image_settings.color_depth = color_depth

        # Set FFMPEG-specific settings if needed
        if file_format == 'FFMPEG':
            scene.render.ffmpeg.format = ffmpeg_format
            scene.render.ffmpeg.codec = ffmpeg_codec
            scene.render.ffmpeg.constant_rate_factor = 'HIGH'
            scene.render.ffmpeg.video_bitrate = 6000
            scene.render.ffmpeg.minrate = 0
            scene.render.ffmpeg.maxrate = 9000
            scene.render.ffmpeg.buffersize = 224 * 8
            scene.render.ffmpeg.packetsize = 2048
            scene.render.ffmpeg.gopsize = 12
            scene.render.ffmpeg.use_max_b_frames = True
            scene.render.ffmpeg.audio_codec = 'AAC'

        if verbose:
            print(f"Render settings applied: {resolution_x}x{resolution_y} @ {fps}fps, format={file_format}, output='{output_path}'")
    except Exception as e:
        if verbose:
            print(f"Failed to set render settings: {e}")

