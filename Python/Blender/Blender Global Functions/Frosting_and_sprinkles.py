import bpy # type: ignore
import random
from typing import Tuple, Optional, List

def add_icing_and_sprinkles(
    donut_obj: bpy.types.Object,
    icing_color: Tuple[float, float, float, float] = (0.95, 0.6, 0.8, 1.0),
    icing_thickness: float = 0.07,
    sprinkle_count: int = 150,
    sprinkle_colors: Optional[List[Tuple[float, float, float]]] = None,
    sprinkle_size: float = 0.04,
    sprinkle_length: float = 0.12,
    seed: Optional[int] = None
) -> Tuple[Optional[bpy.types.Object], Optional[bpy.types.Collection]]:
    """
    Adds a realistic icing layer and sprinkles to the provided donut object.

    Args:
        donut_obj (bpy.types.Object): The donut mesh to add icing and sprinkles to.
        icing_color (tuple): RGBA color for the icing.
        icing_thickness (float): Thickness of the icing layer.
        sprinkle_count (int): Number of sprinkles to add.
        sprinkle_colors (list): List of RGB tuples for sprinkle colors.
        sprinkle_size (float): Diameter of each sprinkle.
        sprinkle_length (float): Length of each sprinkle (for capsule/cylinder shape).
        seed (int, optional): Random seed for reproducibility.

    Returns:
        (icing_obj, sprinkles_collection): The icing mesh object and the sprinkles collection.
    """
    try:
        if seed is not None:
            random.seed(seed)

        # --- Create Icing Layer ---
        bpy.ops.object.select_all(action='DESELECT')
        donut_obj.select_set(True)
        bpy.context.view_layer.objects.active = donut_obj
        bpy.ops.object.duplicate()
        icing = bpy.context.active_object
        icing.name = f"{donut_obj.name}_Icing"

        # Edit icing mesh: keep only top faces, shrink/fatten for thickness
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_random(percent=60, seed=random.randint(0, 100))
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.shrink_fatten(value=icing_thickness)
        bpy.ops.object.mode_set(mode='OBJECT')

        # --- Icing Material ---
        icing_mat = bpy.data.materials.new(name="IcingMaterial")
        icing_mat.use_nodes = True
        nodes = icing_mat.node_tree.nodes
        links = icing_mat.node_tree.links
        nodes.clear()
        output = nodes.new("ShaderNodeOutputMaterial")
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        bsdf.inputs['Base Color'].default_value = icing_color
        bsdf.inputs['Roughness'].default_value = 0.25
        bsdf.inputs['Subsurface'].default_value = 0.1
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        icing.data.materials.clear()
        icing.data.materials.append(icing_mat)
        icing.parent = donut_obj

        # --- Create Sprinkles Collection ---
        sprinkles_collection = bpy.data.collections.new(f"{donut_obj.name}_Sprinkles")
        bpy.context.scene.collection.children.link(sprinkles_collection)

        # Default sprinkle colors if not provided
        if not sprinkle_colors:
            sprinkle_colors = [
                (1.0, 0.2, 0.2),  # Red
                (0.2, 1.0, 0.2),  # Green
                (0.2, 0.2, 1.0),  # Blue
                (1.0, 1.0, 0.2),  # Yellow
                (1.0, 0.5, 0.1),  # Orange
                (1.0, 1.0, 1.0),  # White
                (0.8, 0.2, 0.8),  # Purple
            ]

        # --- Generate Sprinkles ---
        for i in range(sprinkle_count):
            # Sprinkle shape: capsule (cylinder with hemispherical ends)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=sprinkle_size/2, location=(0,0,0))
            sphere1 = bpy.context.active_object
            bpy.ops.mesh.primitive_cylinder_add(
                radius=sprinkle_size / 2,
                depth=sprinkle_length,
                location=(0, 0, 0)
            )
            cylinder = bpy.context.active_object
            bpy.ops.mesh.primitive_uv_sphere_add(radius=sprinkle_size/2, location=(0,0,sprinkle_length/2))
            sphere2 = bpy.context.active_object

            # Join the three parts into one sprinkle
            bpy.ops.object.select_all(action='DESELECT')
            cylinder.select_set(True)
            sphere1.select_set(True)
            sphere2.select_set(True)
            bpy.context.view_layer.objects.active = cylinder
            bpy.ops.object.join()
            sprinkle = bpy.context.active_object
            sprinkle.name = f"Sprinkle_{i:03d}"

            # Randomly position on icing surface (approximate, for perfection use particle system)
            angle = random.uniform(0, 2 * 3.14159)
            ring = random.uniform(donut_obj.dimensions.x * 0.35, donut_obj.dimensions.x * 0.48)
            x = donut_obj.location.x + ring * random.uniform(0.95, 1.05) * (random.uniform(-1, 1))
            y = donut_obj.location.y + ring * random.uniform(0.95, 1.05) * (random.uniform(-1, 1))
            z = donut_obj.location.z + random.uniform(icing_thickness * 0.7, icing_thickness * 1.2) + donut_obj.dimensions.z / 2

            sprinkle.location = (x, y, z)
            sprinkle.rotation_euler = (
                random.uniform(0, 3.14159),
                random.uniform(0, 3.14159),
                random.uniform(0, 3.14159)
            )

            # Sprinkle material
            color = random.choice(sprinkle_colors)
            sprinkle_mat = bpy.data.materials.new(name=f"SprinkleMat_{i:03d}")
            sprinkle_mat.use_nodes = True
            snodes = sprinkle_mat.node_tree.nodes
            slinks = sprinkle_mat.node_tree.links
            snodes.clear()
            soutput = snodes.new("ShaderNodeOutputMaterial")
            sbsdf = snodes.new("ShaderNodeBsdfPrincipled")
            sbsdf.inputs['Base Color'].default_value = (*color, 1.0)
            sbsdf.inputs['Roughness'].default_value = 0.35
            slinks.new(sbsdf.outputs['BSDF'], soutput.inputs['Surface'])
            sprinkle.data.materials.clear()
            sprinkle.data.materials.append(sprinkle_mat)

            # Move sprinkle to sprinkles collection
            bpy.ops.collection.objects_remove_all()
            sprinkles_collection.objects.link(sprinkle)
            sprinkle.parent = icing

        print(f"Icing and {sprinkle_count} sprinkles added to '{donut_obj.name}'.")
        return icing, sprinkles_collection

    except Exception as e:
        print(f"Failed to add icing and sprinkles: {e}")
        return None, None

# Usage example:
# donut = add_donut()
# add_icing_and_sprinkles(donut)