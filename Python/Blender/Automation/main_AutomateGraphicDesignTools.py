import sys
import os

# Update this path to the directory containing your Blender global function scripts
SCRIPT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../Blender Global Functions")
)
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from Blender_clear_scene_function import clear_scene  # Ensure the file 'Blender_clear_scene_function.py' exists in '../Blender Global Functions'
from Add_ground_function import add_ground
from Add_donut_function import add_donut
from Add_camera_function import add_camera
from Add_light_functoin import add_light
from Set_render_settings_function import set_render_settings
from Bake_physics_funtion import bake_physics
from Render_animation_functoin import render_animation

output_path = "/tmp/render_output"  # Set your desired output path here

def main():
    clear_scene(verbose=True)
    ground = add_ground()
    donut = add_donut()
    camera = add_camera()
    light = add_light()
    set_render_settings(output_path)
    bake_physics()
    render_animation()
    print("Script ran successfully!")

if __name__ == "__main__":
    main()