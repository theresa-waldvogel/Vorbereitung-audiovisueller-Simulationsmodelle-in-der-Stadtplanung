import bpy
from collections import defaultdict
import re

def remove_numeric_parts(name):
    """Remove numeric parts from a material name for comparison."""
    return re.sub(r'\d+', '', name)

def find_similar_materials():
    materials = bpy.data.materials
    material_groups = defaultdict(list)
    
    # Create a list of material names
    material_names = [mat.name for mat in materials]
    
    for i, mat in enumerate(material_names):
        base_name_i = remove_numeric_parts(mat)
        for j, other_mat in enumerate(material_names):
            if i < j:
                base_name_j = remove_numeric_parts(other_mat)
                if base_name_i == base_name_j:
                    material_groups[mat].append(other_mat)
                    material_groups[other_mat].append(mat)  # Ensure bidirectional linking

    # Combine groups that share members into a final grouping
    final_groups = defaultdict(set)
    visited = set()

    for key, group in material_groups.items():
        if key not in visited:
            combined_group = set(group)
            combined_group.add(key)
            for member in group:
                combined_group.update(material_groups[member])
            for member in combined_group:
                visited.add(member)
            final_groups[key] = combined_group

    return final_groups

def assign_grouped_materials():
    grouped_materials = find_similar_materials()
    
    for group, materials in grouped_materials.items():
        # Create a new material for the group
        new_material_name = f"{remove_numeric_parts(group)}_Group"
        new_material = bpy.data.materials.new(name=new_material_name)
        
        # Get all objects with the materials in the group
        objects_to_update = set()
        for mat_name in materials:
            material = bpy.data.materials.get(mat_name)
            if material:
                for obj in bpy.data.objects:
                    if obj.type == 'MESH' and any(m.name == mat_name for m in obj.data.materials):
                        objects_to_update.add(obj)
        
        # Assign the new material to these objects
        for obj in objects_to_update:
            for i, mat in enumerate(obj.data.materials):
                if mat.name in materials:
                    obj.data.materials[i] = new_material

assign_grouped_materials()
