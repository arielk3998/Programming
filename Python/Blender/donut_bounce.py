import bpy
import math

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Set up the scene
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 100

# Add a plane (ground)
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"

# Add a torus (donut)
bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.4, location=(0, 0, 2))
donut = bpy.context.active_object
donut.name = "Donut"

# Add a simple pink material to the donut
mat = bpy.data.materials.new(name="DonutMaterial")
mat.diffuse_color = (1.0, 0.5, 0.7, 1.0)
donut.data.materials.append(mat)

# Animate the donut bouncing
bounce_heights = [2, 1.5, 1, 0.5, 0.2]
frame = 1
for i, height in enumerate(bounce_heights):
    # Up
    donut.location.z = height
    donut.keyframe_insert(data_path="location", frame=frame)
    # Down
    frame += 10
    donut.location.z = 0.5
    donut.keyframe_insert(data_path="location", frame=frame)
    frame += 10

# Add a camera
bpy.ops.object.camera_add(location=(5, -5, 5), rotation=(math.radians(60), 0, math.radians(45)))
camera = bpy.context.active_object
scene.camera = camera

# Add a light
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))

print("Donut bounce scene created!")