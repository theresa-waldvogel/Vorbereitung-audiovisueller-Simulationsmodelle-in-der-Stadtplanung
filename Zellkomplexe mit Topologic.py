import bpy
import bmesh
import math
import os

# Function to combine multiple objects into a single mesh
def combine_objects_to_mesh(objects, name):
    # Create a new mesh and object
    combined_mesh = bpy.data.meshes.new(name + '_CombinedMesh')
    combined_object = bpy.data.objects.new(name + '_CombinedObject', combined_mesh)

    # Get or create a collection named 'Gebäude'
    collection = bpy.data.collections.get('Gebäude')
    if not collection:
        collection = bpy.data.collections.new('Gebäude')
        bpy.context.scene.collection.children.link(collection)
    collection.objects.link(combined_object)

    materials = []
    material_index_map = {}

    vertices = []
    edges = []
    faces = []
    face_materials = []

    vertex_offset = 0

    for obj in objects:
        if obj.type == 'MESH':
            mesh = obj.data

            # Merge triangles before processing
            merge_triangles(mesh)

            # Collect materials and their indices
            for mat in obj.material_slots:
                if mat.material not in materials:
                    materials.append(mat.material)
                material_index_map[mat.material] = materials.index(mat.material)

            # Transform vertices to world coordinates and add to list
            for vert in mesh.vertices:
                vertices.append(obj.matrix_world @ vert.co)

            # Transform edges and add to list
            for edge in mesh.edges:
                edges.append((edge.vertices[0] + vertex_offset, edge.vertices[1] + vertex_offset))

            # Transform faces, collect material indices and add to list
            for poly in mesh.polygons:
                face = [vertex_index + vertex_offset for vertex_index in poly.vertices]
                faces.append(face)
                face_materials.append(material_index_map[obj.material_slots[poly.material_index].material])

            # Update vertex offset for next object
            vertex_offset += len(mesh.vertices)

    # Create the new mesh from collected vertices, edges, and faces
    combined_mesh.from_pydata(vertices, edges, faces)
    combined_mesh.update()

    # Assign collected materials to the new mesh
    for mat in materials:
        combined_object.data.materials.append(mat)

    # Assign material indices to faces
    for poly, mat_index in zip(combined_mesh.polygons, face_materials):
        poly.material_index = mat_index

    return combined_object, combined_mesh

# Function to merge triangles in a mesh
def merge_triangles(mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Dissolve edges based on a small angle limit to merge triangles
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(1.0), verts=bm.verts, edges=bm.edges, delimit={'NORMAL'})

    bm.to_mesh(mesh)
    bm.free()

# Function to filter faces in a mesh
def filter_faces(mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Find the highest and lowest z-coordinate
    z_coords = [v.co.z for v in bm.verts]
    min_z = min(z_coords)
    max_z = max(z_coords)

    faces_to_keep = []
    for face in bm.faces:
        # Calculate face normal
        face_normal = face.normal
        # Check if the face is horizontal
        if math.isclose(abs(face_normal.z), 1.0, abs_tol=1e-5):
            face_center_z = sum([v.co.z for v in face.verts]) / len(face.verts)
            if math.isclose(face_center_z, min_z, abs_tol=1e-5) or math.isclose(face_center_z, max_z, abs_tol=1e-5):
                faces_to_keep.append(face)
        else:
            faces_to_keep.append(face)

    # Delete faces not in the list of faces to keep
    faces_to_delete = [face for face in bm.faces if face not in faces_to_keep]
    bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')

    bm.to_mesh(mesh)
    bm.free()

# Function to group objects by their parent
def group_objects_by_parent(objects):
    groups = {}
    for obj in objects:
        parent_name = obj.parent.name if obj.parent else obj.name
        if parent_name not in groups:
            groups[parent_name] = []
        groups[parent_name].append(obj)
    return groups

# Function to process a group of objects
def process_group(objects, name):
    combined_object, combined_mesh = combine_objects_to_mesh(objects, name)
    filter_faces(combined_mesh)

    # Delete original objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.ops.object.delete()

    # Select only the combined object
    bpy.ops.object.select_all(action='DESELECT')
    combined_object.select_set(True)
    bpy.context.view_layer.objects.active = combined_object

# Main function to execute the script
def main():
    selected_objects = bpy.context.selected_objects

    if not selected_objects:
        print("Please select multiple mesh objects.")
        return

    # Group objects by their parent and process each group
    groups = group_objects_by_parent(selected_objects)
    for group_name, group_objects in groups.items():
        process_group(group_objects, group_name)

# Run the main function
main()
