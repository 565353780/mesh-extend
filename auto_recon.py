import sys
sys.path.append('../wn-nc/')

import os

from mesh_extend.Method.filter import filterMesh
from mesh_extend.Method.merge import mergeMesh
from mesh_extend.Module.mesh_splitter import MeshSplitter
from mesh_extend.Module.mesh_reconstructor import MeshReconstructor


if __name__ == '__main__':
    home = os.environ['HOME']
    mesh_file_path = home + "/chLi/Dataset/ShuMei/output_039.glb"
    save_submesh_folder_path = "./output/submesh2/"
    triangle_num_min = 1000
    save_valid_submesh_folder_path = "./output/submesh2_valid/"
    save_recon_mesh_folder_path = "./output/recon_mesh2/"
    save_merge_mesh_file_path = './output/merge_mesh2.ply'

    '''
    mesh_splitter = MeshSplitter(mesh_file_path)
    submeshes = mesh_splitter.splitMesh()
    mesh_splitter.saveSubMeshes(submeshes, save_submesh_folder_path)

    filterMesh(
        save_submesh_folder_path,
        triangle_num_min,
        save_valid_submesh_folder_path,
    )

    mesh_reconstructor = MeshReconstructor()
    mesh_reconstructor.reconMeshFolder(save_submesh_folder_path, save_recon_mesh_folder_path)
    '''

    mergeMesh(save_recon_mesh_folder_path, save_merge_mesh_file_path)
