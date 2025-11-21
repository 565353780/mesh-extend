import os
import open3d as o3d

from mesh_extend.Method.path import createFileFolder

def mergeMesh(mesh_folder_path: str, save_merge_mesh_file_path: str) -> bool:
    merge_mesh = o3d.geometry.TriangleMesh()

    mesh_filename_list = os.listdir(mesh_folder_path)

    for mesh_filename in mesh_filename_list:
        if mesh_filename.split('.')[-1] not in ['ply', 'obj']:
            continue

        mesh_file_path = mesh_folder_path + mesh_filename
        mesh = o3d.io.read_triangle_mesh(mesh_file_path)

        merge_mesh += mesh

    createFileFolder(save_merge_mesh_file_path)
    o3d.io.write_triangle_mesh(save_merge_mesh_file_path, merge_mesh, write_ascii=True)
    return True
