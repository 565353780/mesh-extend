import os
import open3d as o3d

mesh_folder_path = './output/recon_mesh/'

merge_mesh = o3d.geometry.TriangleMesh()

mesh_filename_list = os.listdir(mesh_folder_path)

for mesh_filename in mesh_filename_list:
    if mesh_filename.split('.')[-1] not in ['ply', 'obj']:
        continue

    mesh_file_path = mesh_folder_path + mesh_filename
    mesh = o3d.io.read_triangle_mesh(mesh_file_path)

    merge_mesh += mesh

o3d.io.write_triangle_mesh('./output/merge_mesh.ply', merge_mesh, write_ascii=True)
