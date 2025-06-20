"""
================================================================================
Blender Donut Scene Automation Script
================================================================================

This script automates the creation of a photorealistic donut scene in Blender,
including ground, donut, camera, lighting, physics baking, and rendering.
It demonstrates modular, robust, and readable Blender scripting practices.

Features:
- Clears the scene for a fresh start.
- Adds a ground plane, realistic donut, camera, and lighting.
- Adds a perfect icing layer and sprinkles to the donut.
- Animates the camera with an anime-style fly-through (if available).
- Sets up render settings and output path.
- Bakes physics for realism.
- Renders the animation to the specified output directory.
- Prints clear progress and completion messages.

================================================================================
"""

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
from Add_camera_function import add_camera, animate_camera_fly_through  # type: ignore
from Add_light_function import add_light  # type: ignore
from Add_ground_function import add_ground  # type: ignore
from Set_render_settings_function import set_render_settings  # type: ignore
from Bake_physics_function import bake_physics  # type: ignore
from Render_animation_function import render_animation  # type: ignore
from Frosting_and_sprinkles import add_icing_and_sprinkles  # type: ignore

OUTPUT_PATH = "/tmp/render_output"  # Set your desired output path here

def main():
    print("=== Blender Donut Scene Automation Started ===")
    try:
        clear_scene(verbose=True)
        print("Scene cleared.")

        ground = add_ground()
        print("Ground added.")

        donut = add_donut()
        print("Donut added.")

        # Add icing and sprinkles to the donut
        try:
            icing, sprinkles = add_icing_and_sprinkles(donut)
            if icing and sprinkles:
                print("Icing and sprinkles added.")
            else:
                print("Icing and sprinkles could not be added.")
        except Exception as e:
            print(f"Icing and sprinkles skipped or failed: {e}")

        camera = add_camera()
        print("Camera added.")

        # Animate camera if function is available
        try:
            animate_camera_fly_through(camera, donut)
            print("Camera animation applied (anime-style fly-through).")
        except Exception as e:
            print(f"Camera animation skipped or failed: {e}")

        light = add_light()
        print("Lighting added.")

        set_render_settings(OUTPUT_PATH)
        print(f"Render settings configured. Output path: {OUTPUT_PATH}")

        bake_physics()
        print("Physics baked.")

        render_animation()
        print("Rendering animation...")

        print("\n=== Script ran successfully! ===")
        print(f"Your animation will be saved to: {OUTPUT_PATH}")
        print("Check Blender's Render Properties for the exact output file name and format.")
    except Exception as e:
        print(f"\n[ERROR] Script failed: {e}")

if __name__ == "__main__":
    main()