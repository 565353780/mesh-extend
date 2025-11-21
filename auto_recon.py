import sys
sys.path.append('../wn-nc/')

import os

from mesh_extend.Module.mesh_splitter import MeshSplitter
from mesh_extend.Module.mesh_reconstructor import MeshReconstructor

if __name__ == '__main__':
    home = os.environ['HOME']
    mesh_file_path = home + "/chLi/Dataset/ShuMei/output_039.glb"
    save_submesh_folder_path = "./output/submesh2/"
    save_recon_mesh_folder_path = "./output/recon_mesh2/"

    mesh_splitter = MeshSplitter(mesh_file_path)
    submeshes = mesh_splitter.splitMesh()

    mesh_splitter.saveSubMeshes(submeshes, save_submesh_folder_path)

    mesh_reconstructor = MeshReconstructor()
    recon_meshes = mesh_reconstructor.reconMeshFolder(save_submesh_folder_path)
    mesh_reconstructor.saveReconMeshDict(recon_meshes, save_recon_mesh_folder_path)
