import os
import numpy as np
import open3d as o3d
from shutil import copyfile


def filterMesh(
    mesh_folder_path: str,
    triangle_num_min: int,
    save_mesh_folder_path: str,
) -> bool:
    mesh_filename_list = os.listdir(mesh_folder_path)

    os.makedirs(save_mesh_folder_path, exist_ok=True)

    for mesh_filename in mesh_filename_list:
        if mesh_filename.split('.')[-1] not in ['ply', 'obj']:
            continue

        mesh_file_path = mesh_folder_path + mesh_filename
        mesh = o3d.io.read_triangle_mesh(mesh_file_path)

        triangles = np.asarray(mesh.triangles)

        print(triangles.shape[0])

        if triangles.shape[0] < triangle_num_min:
            continue

        curr_mesh_file_path = mesh_folder_path + mesh_filename
        curr_save_mesh_file_path = save_mesh_folder_path + mesh_filename
        copyfile(curr_mesh_file_path, curr_save_mesh_file_path)
    return True
