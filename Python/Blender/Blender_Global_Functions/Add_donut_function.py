import bpy  # type: ignore
import random
from typing import Tuple, Optional

def add_donut(
    location: Tuple[float, float, float] = (0.0, 0.0, 3.0),
    major_radius: float = 1.0,
    minor_radius: float = 0.4,
    name: str = "Donut",
    rigid_body: bool = True,
    mass: float = 1.0,
    friction: float = 0.5,
    restitution: float = 0.7,
    smooth_shading: bool = True,
    subdivision_levels: int = 2,
    material_color: Tuple[float, float, float, float] = (0.9, 0.6, 0.3, 1.0),
    roughness: float = 0.4,
    subsurface: float = 0.2,
    material_name: str = "DonutMaterial"
) -> Optional[bpy.types.Object]:
    """
    Adds a photorealistic donut mesh to the scene with procedural bread texture,
    frosting, and optional rigid body physics. Includes natural imperfections.

    Returns:
        The donut object, or None if creation failed.
    """
    try:
        # Store current selection and mode
        prev_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
        bpy.ops.object.select_all(action='DESELECT')

        # --- Create Donut Base ---
        bpy.ops.mesh.primitive_torus_add(
            major_radius=major_radius,
            minor_radius=minor_radius,
            location=location
        )
        donut = bpy.context.active_object
        donut.name = name

        # --- Add Rigid Body Physics ---
        if rigid_body:
            bpy.ops.rigidbody.object_add()
            donut.rigid_body.type = 'ACTIVE'
            donut.rigid_body.mass = mass
            donut.rigid_body.friction = friction
            donut.rigid_body.restitution = restitution

        # --- Smooth Shading & Subdivision ---
        if smooth_shading:
            bpy.ops.object.shade_smooth()
        subdiv = donut.modifiers.new(name="Subdivision", type='SUBSURF')
        subdiv.levels = subdivision_levels
        subdiv.render_levels = subdivision_levels

        # --- Add Subtle Imperfections (Displacement Modifier) ---
        tex = bpy.data.textures.new("DonutImperfection", type='CLOUDS')
        disp = donut.modifiers.new(name="Imperfection", type='DISPLACE')
        disp.texture = tex
        disp.strength = 0.07  # Subtle, tweak for more/less bump

        # --- Bread Material (Procedural) ---
        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Nodes for bread
        output = nodes.new("ShaderNodeOutputMaterial")
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        noise = nodes.new("ShaderNodeTexNoise")
        bump = nodes.new("ShaderNodeBump")
        colorramp = nodes.new("ShaderNodeValToRGB")
        mapping = nodes.new("ShaderNodeMapping")
        texcoord = nodes.new("ShaderNodeTexCoord")

        # Bread color ramp (golden brown)
        colorramp.color_ramp.elements[0].color = (0.92, 0.75, 0.45, 1)
        colorramp.color_ramp.elements[1].color = (0.7, 0.5, 0.2, 1)

        # Node links for bread
        links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
        noise.inputs['Scale'].default_value = 8.0
        links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
        links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(noise.outputs['Fac'], bump.inputs['Height'])
        bump.inputs['Strength'].default_value = 0.15
        links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
        bsdf.inputs['Subsurface'].default_value = 0.25
        bsdf.inputs['Subsurface Color'].default_value = (1, 0.8, 0.6, 1)
        bsdf.inputs['Roughness'].default_value = 0.45
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

        donut.data.materials.clear()
        donut.data.materials.append(mat)

        # --- Frosting Geometry ---
        bpy.ops.object.select_all(action='DESELECT')
        donut.select_set(True)
        bpy.context.view_layer.objects.active = donut
        bpy.ops.object.duplicate()
        frosting = bpy.context.active_object
        frosting.name = f"{name}_Frosting"

        # Edit frosting mesh: keep only top faces, shrink/fatten for thickness
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_random(percent=60, seed=random.randint(0, 100))
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.shrink_fatten(value=0.07)
        bpy.ops.object.mode_set(mode='OBJECT')

        # --- Frosting Material (Procedural) ---
        frosting_mat = bpy.data.materials.new(name="FrostingMaterial")
        frosting_mat.use_nodes = True
        f_nodes = frosting_mat.node_tree.nodes
        f_links = frosting_mat.node_tree.links
        f_nodes.clear()

        f_output = f_nodes.new("ShaderNodeOutputMaterial")
        f_bsdf = f_nodes.new("ShaderNodeBsdfPrincipled")
        f_noise = f_nodes.new("ShaderNodeTexNoise")
        f_bump = f_nodes.new("ShaderNodeBump")
        f_colorramp = f_nodes.new("ShaderNodeValToRGB")
        f_mapping = f_nodes.new("ShaderNodeMapping")
        f_texcoord = f_nodes.new("ShaderNodeTexCoord")

        # Frosting color ramp (pink gradient)
        f_colorramp.color_ramp.elements[0].color = (0.95, 0.6, 0.8, 1)
        f_colorramp.color_ramp.elements[1].color = (0.8, 0.2, 0.4, 1)

        f_links.new(f_texcoord.outputs['Object'], f_mapping.inputs['Vector'])
        f_links.new(f_mapping.outputs['Vector'], f_noise.inputs['Vector'])
        f_noise.inputs['Scale'].default_value = 12.0
        f_links.new(f_noise.outputs['Fac'], f_colorramp.inputs['Fac'])
        f_links.new(f_colorramp.outputs['Color'], f_bsdf.inputs['Base Color'])
        f_links.new(f_noise.outputs['Fac'], f_bump.inputs['Height'])
        f_bump.inputs['Strength'].default_value = 0.08
        f_links.new(f_bump.outputs['Normal'], f_bsdf.inputs['Normal'])
        f_bsdf.inputs['Roughness'].default_value = 0.25
        f_bsdf.inputs['Subsurface'].default_value = 0.1
        f_links.new(f_bsdf.outputs['BSDF'], f_output.inputs['Surface'])

        frosting.data.materials.clear()
        frosting.data.materials.append(frosting_mat)
        frosting.parent = donut

        # --- Restore previous mode ---
        bpy.ops.object.select_all(action='DESELECT')
        donut.select_set(True)
        bpy.context.view_layer.objects.active = donut
        if prev_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=prev_mode)

        print("Donut creation complete! Reminder: Your render will be saved to the output path set in Blender's Render Properties (default: //render.png).")
        return donut

    except Exception as e:
        print(f"Failed to add donut: {e}")
        return None

# Usage:
# donut = add_donut()
