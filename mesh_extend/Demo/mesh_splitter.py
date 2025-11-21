import os
import open3d as o3d

from mesh_extend.Module.mesh_splitter import MeshSplitter

def demo():
    home = os.environ['HOME']
    mesh_file_path = home + "/chLi/Dataset/ShuMei/split_results.glb"
    save_submesh_folder_path = "./output/submesh/"

    mesh_splitter = MeshSplitter(mesh_file_path)
    submeshes = mesh_splitter.splitMesh()

    mesh_splitter.saveSubMeshes(submeshes, save_submesh_folder_path)

    print(f"分割成 {len(submeshes)} 个连通子网格")
    # o3d.visualization.draw_geometries(submeshes)
    return True
