import bpy
import math

class SCENEGENERATOR_PT_panel(bpy.types.Panel):
    bl_label = "Scene Generator"
    bl_idname = "SCENEGENERATOR_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SceneGen"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Generate a Donut Scene")
        layout.operator("scene.generate_donut", text="Generate Donut with Physics")

class SCENEGENERATOR_OT_generate_donut(bpy.types.Operator):
    bl_idname = "scene.generate_donut"
    bl_label = "Generate Donut with Physics"

    def execute(self, context):
        # Clear existing mesh objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Add ground plane
        bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
        ground = bpy.context.active_object
        ground.name = "Ground"
        bpy.ops.rigidbody.object_add()
        ground.rigid_body.type = 'PASSIVE'
        ground.rigid_body.friction = 0.5
        ground.rigid_body.restitution = 0.7

        # Add donut (torus)
        bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.4, location=(0, 0, 3))
        donut = bpy.context.active_object
        donut.name = "Donut"
        bpy.ops.rigidbody.object_add()
        donut.rigid_body.type = 'ACTIVE'
        donut.rigid_body.mass = 1.0
        donut.rigid_body.friction = 0.5
        donut.rigid_body.restitution = 0.7

        # Smooth shading
        bpy.ops.object.shade_smooth()

        # Add a simple pink material to the donut
        mat = bpy.data.materials.new(name="DonutMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (1.0, 0.5, 0.7, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.4
        donut.data.materials.append(mat)

        # Add camera
        bpy.ops.object.camera_add(location=(5, -5, 5), rotation=(math.radians(60), 0, math.radians(45)))
        camera = bpy.context.active_object
        bpy.context.scene.camera = camera

        # Add a sun light
        bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))

        # Set up rigid body world for physics simulation
        if not bpy.context.scene.rigidbody_world:
            bpy.ops.rigidbody.world_add()
        bpy.context.scene.rigidbody_world.steps_per_second = 120
        bpy.context.scene.rigidbody_world.solver_iterations = 25

        # Set animation frames
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 100

        self.report({'INFO'}, "Donut scene with physics generated!")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SCENEGENERATOR_PT_panel)
    bpy.utils.register_class(SCENEGENERATOR_OT_generate_donut)

def unregister():
    bpy.utils.unregister_class(SCENEGENERATOR_PT_panel)
    bpy.utils.unregister_class(SCENEGENERATOR_OT_generate_donut)

if __name__ == "__main__":
    register()