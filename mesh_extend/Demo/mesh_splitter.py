import os
import open3d as o3d

from mesh_extend.Module.mesh_splitter import MeshSplitter

def demo():
    mesh_file_path = "/Users/chli/Downloads/split_results.glb"

    mesh_splitter = MeshSplitter(mesh_file_path)
    submeshes = mesh_splitter.splitMesh()

    # 打印结果
    print(f"分割成 {len(submeshes)} 个连通子网格")

    # 可视化
    o3d.visualization.draw_geometries(submeshes)

    os.makedirs('./output/', exist_ok=True)
    # 保存结果
    for i, submesh in enumerate(submeshes):
        o3d.io.write_triangle_mesh(f"./output/submesh_{i}.ply", submesh)
    return True
