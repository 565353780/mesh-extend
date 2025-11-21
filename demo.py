import os
import numpy as np
import open3d as o3d
from tqdm import tqdm, trange
from typing import List
from collections import deque


def split_into_connected_components(
    mesh: o3d.geometry.TriangleMesh
) -> List[o3d.geometry.TriangleMesh]:
    vertices = np.asarray(mesh.vertices)
    triangles = np.asarray(mesh.triangles)

    # Step 1: 构建边到三角形的映射 (关键！用边当桥梁)
    edge_to_tri = {}
    print(' start construct VE map...')
    for tri_idx, tri in enumerate(tqdm(triangles)):
        v0, v1, v2 = tri
        # 每条边标准化为 (min, max) 保证无序
        edges = [
            (min(v0, v1), max(v0, v1)),
            (min(v1, v2), max(v1, v2)),
            (min(v2, v0), max(v2, v0))
        ]
        for e in edges:
            if e not in edge_to_tri:
                edge_to_tri[e] = []
            edge_to_tri[e].append(tri_idx)

    # Step 2: 构建三角形邻接表 (用BFS找连通块)
    n_tri = len(triangles)
    adj = [[] for _ in range(n_tri)]
    for e, tri_list in edge_to_tri.items():
        if len(tri_list) == 2:  # 只有内部边才连通两个三角形
            i, j = tri_list
            adj[i].append(j)
            adj[j].append(i)

    # Step 3: BFS找所有连通分量
    visited = [False] * n_tri
    submeshes = []
    print(' start search connected component...')
    for i in trange(n_tri):
        if not visited[i]:
            # BFS遍历当前连通块
            comp_tri_indices = []
            queue = deque([i])
            visited[i] = True
            while queue:
                idx = queue.popleft()
                comp_tri_indices.append(idx)
                for neighbor in adj[idx]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
            
            # Step 4: 为当前连通块提取顶点和三角形
            all_vertex_indices = set()
            for tri_idx in comp_tri_indices:
                all_vertex_indices.update(triangles[tri_idx])
            all_vertex_indices = sorted(all_vertex_indices)  # 统一顶点顺序
            
            # 创建顶点索引映射 (原索引 -> 新索引)
            vertex_map = {orig_idx: new_idx for new_idx, orig_idx in enumerate(all_vertex_indices)}
            
            # 构建新顶点坐标和三角形索引
            new_vertices = vertices[all_vertex_indices]  # 形状 (K, 3)
            new_triangles = np.array([
                [vertex_map[v] for v in triangles[tri_idx]] 
                for tri_idx in comp_tri_indices
            ], dtype=np.int32)
            
            # Step 5: 转成Open3D的TriangleMesh (最后一步才用Open3D)
            mesh = o3d.geometry.TriangleMesh()
            mesh.vertices = o3d.utility.Vector3dVector(new_vertices)
            mesh.triangles = o3d.utility.Vector3iVector(new_triangles)
            submeshes.append(mesh)
    
    return submeshes


# 使用示例
if __name__ == "__main__":
    # 读取网格
    mesh = o3d.io.read_triangle_mesh("/Users/chli/Downloads/split_results.glb")
    mesh.compute_vertex_normals()

    # 按连通性分割
    submeshes = split_into_connected_components(mesh)

    # 打印结果
    print(f"分割成 {len(submeshes)} 个连通子网格")

    # 可视化
    o3d.visualization.draw_geometries(submeshes)

    os.makedirs('./output/', exist_ok=True)
    # 保存结果
    for i, submesh in enumerate(submeshes):
        o3d.io.write_triangle_mesh(f"./output/submesh_{i}.ply", submesh)
    exit()

    pcd = o3d.geometry.PointCloud()
    pcd.points = mesh.vertices
    pcd.normals = mesh.vertex_normals

    extend_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, 
        depth=10  # 控制重建的精细度，值越大越精细
    )

    extend_mesh.compute_vertex_normals()
    extend_mesh.paint_uniform_color([0, 1, 0])

    extend_mesh.translate([0, 1.5, 0])

    # 保存结果
    o3d.visualization.draw_geometries([mesh, extend_mesh])
    o3d.io.write_triangle_mesh("reconstructed_mesh.ply", mesh)
