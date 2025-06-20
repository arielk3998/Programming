import bpy
import math
import os

try:
    # Clear existing objects
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

    # Smooth shading and subdivision
    bpy.ops.object.shade_smooth()
    subdiv = donut.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 2

    # Add a realistic material to the donut
    mat = bpy.data.materials.new(name="DonutMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.9, 0.6, 0.3, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.4
        if "Subsurface" in bsdf.inputs:
            bsdf.inputs["Subsurface"].default_value = 0.2
    if len(donut.data.materials) == 0:
        donut.data.materials.append(mat)
    else:
        donut.data.materials[0] = mat

    # Add camera with depth of field
    bpy.ops.object.camera_add(location=(5, -5, 5), rotation=(math.radians(60), 0, math.radians(45)))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera
    camera.data.dof.use_dof = True
    camera.data.dof.focus_distance = 5
    camera.data.dof.aperture_fstop = 2.8

    # Add an area light
    bpy.ops.object.light_add(type='AREA', location=(4, -4, 6))
    light = bpy.context.active_object
    light.data.energy = 1000
    light.data.size = 5

    # Set up rigid body world for physics simulation
    if not bpy.context.scene.rigidbody_world:
        bpy.ops.rigidbody.world_add()
    rbw = bpy.context.scene.rigidbody_world
    if hasattr(rbw, "steps_per_second"):
        rbw.steps_per_second = 120
    if hasattr(rbw, "solver_iterations"):
        rbw.solver_iterations = 25

    # Set animation frames
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 100

    # Ensure output directory exists
    output_dir = "/home/spacecadet/Desktop/Master Folder/Ariel's/Repo/Programming/Python/Blender"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    bpy.context.scene.render.filepath = os.path.join(output_dir, "bouncing_donut.mp4")

    # Set render settings
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.fps = 30
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'

    # Bake the physics simulation
    try:
        bpy.ops.ptcache.bake_all(bake=True)
    except Exception as e:
        print("Bake failed:", e)

    # Render animation
    bpy.ops.render.render(animation=True)

    print("Automated bouncing donut scene created and rendered!")

except Exception as e:
    print("Script failed:", e)