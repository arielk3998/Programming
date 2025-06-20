import sys
import os

# Configure the path to include the directory containing Blender global function scripts.
SCRIPT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../Blender Global Functions")
)
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

# ----------------------------------------------------------------------------------------
# Why '# type: ignore' is used on the import statements below:
#
# This script is designed to be executed within Blender's embedded Python environment,
# where custom modules such as 'Blender_clear_scene_function', 'Add_donut_function', etc.,
# are available. However, when editing or linting this script in a standard IDE or outside
# Blender, these modules will not be found, resulting in unresolved import warnings or errors
# from tools like Pyright, mypy, or other static analyzers.
#
# To maintain a clean development experience and prevent these false-positive warnings,
# the '# type: ignore' comment is appended to each import. This instructs type checkers
# and linters to skip type checking for those specific lines. This approach is a best
# practice for Blender scripting projects that depend on Blender-specific or environment-
# specific modules, ensuring compatibility with both Blender and external development tools.
# ----------------------------------------------------------------------------------------

from Blender_clear_scene_function import clear_scene  # type: ignore
from Add_donut_function import add_donut  # type: ignore
from Add_camera_function import add_camera  # type: ignore
from Add_light_functoin import add_light  # type: ignore
from Add_ground_function import add_ground  # type: ignore
from Set_render_settings_function import set_render_settings  # type: ignore
from Bake_physics_funtion import bake_physics  # type: ignore
from Render_animation_functoin import render_animation  # type: ignore

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