import bpy

# Count the used materials
used_materials = set()
for obj in bpy.data.objects:
    if obj.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}:
        for mat_slot in obj.material_slots:
            if mat_slot.material:
                used_materials.add(mat_slot.material)

# delete unused materials
for mat in bpy.data.materials:
    if mat not in used_materials:
        bpy.data.materials.remove(mat)

print("All unused materials have been deleted.")
