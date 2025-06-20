scene_generator.py

import bpy

class SCENEGENERATOR_PT_panel(bpy.types.Panel):
    bl_label = "Scene Generator"
    bl_idname = "SCENEGENERATOR_PT_panel"
    bl_space_type = 'VIEW_3D'         # 3D Viewport
    bl_region_type = 'UI'             # Sidebar
    bl_category = "SceneGen"          # Tab name

    def draw(self, context):
        layout = self.layout
        layout.label(text="Generate a Donut Scene")
        layout.operator("scene.generate_donut", text="Generate Donut")

class SCENEGENERATOR_OT_generate_donut(bpy.types.Operator):
    bl_idname = "scene.generate_donut"
    bl_label = "Generate Donut"

    def execute(self, context):
        # Example: Add a torus (donut)
        bpy.ops.mesh.primitive_torus_add(location=(0, 0, 1))
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SCENEGENERATOR_PT_panel)
    bpy.utils.register_class(SCENEGENERATOR_OT_generate_donut)

def unregister():
    bpy.utils.unregister_class(SCENEGENERATOR_PT_panel)
    bpy.utils.unregister_class(SCENEGENERATOR_OT_generate_donut)

if __name__ == "__main__":
    register()