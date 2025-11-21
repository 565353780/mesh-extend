import sys
sys.path.append('../wn-nc/')

from mesh_extend.Module.mesh_reconstructor import MeshReconstructor

def demo():
    mesh_folder_path = "./output/submesh/"
    save_recon_mesh_folder_path = "./output/recon_mesh/"

    mesh_reconstructor = MeshReconstructor()
    recon_meshes = mesh_reconstructor.reconMeshFolder(mesh_folder_path)
    mesh_reconstructor.saveReconMeshDict(recon_meshes, save_recon_mesh_folder_path)
    return True
