import os
import numpy as np
import open3d as o3d
from tqdm import tqdm, trange
from typing import List, Optional
from collections import deque, defaultdict


class MeshSplitter(object):
    def __init__(self, mesh_file_path: Optional[str] = None) -> None:
        self.mesh: Optional[o3d.geometry.TriangleMesh] = None

        if mesh_file_path is not None:
            self.loadMeshFile(mesh_file_path)
        return

    def loadMeshFile(self, mesh_file_path: str) -> bool:
        if not os.path.exists(mesh_file_path):
            print('[ERROR][MeshSplitter::loadMeshFile]')
            print('\t mesh file not exist!')
            print('\t mesh_file_path:', mesh_file_path)
            return False

        self.mesh = o3d.io.read_triangle_mesh(mesh_file_path)
        return True


    def createVEMap(self, triangles: np.ndarray) -> dict:
        edge_to_tri = defaultdict(list)

        for tri_idx, tri in enumerate(tqdm(triangles, desc="VE Map", unit="tri", disable=False)):
            v0, v1, v2 = tri

            # 边1: v0-v1
            if v0 < v1:
                e0 = (v0, v1)
            else:
                e0 = (v1, v0)

            # 边2: v1-v2
            if v1 < v2:
                e1 = (v1, v2)
            else:
                e1 = (v2, v1)

            # 边3: v2-v0
            if v2 < v0:
                e2 = (v2, v0)
            else:
                e2 = (v0, v2)

            # 直接添加 (defaultdict 自动处理新键)
            edge_to_tri[e0].append(tri_idx)
            edge_to_tri[e1].append(tri_idx)
            edge_to_tri[e2].append(tri_idx)

        return dict(edge_to_tri)

    def createNeighboorTable(self, triangle_num: int, edge_to_tri: dict) -> list:
        adj = [[] for _ in range(triangle_num)]
        for tri_list in edge_to_tri.values():
            if len(tri_list) == 2:  # 只有内部边才连通两个三角形
                i, j = tri_list
                adj[i].append(j)
                adj[j].append(i)
        return adj

    def splitMesh(self) -> List[o3d.geometry.TriangleMesh]:
        if self.mesh is None:
            print('[ERROR][MeshSplitter::splitMesh]')
            print('\t mesh not exist! please load mesh first')
            return []

        vertices = np.asarray(self.mesh.vertices)
        triangles = np.asarray(self.mesh.triangles)

        triangle_num = triangles.shape[0]

        edge_to_tri = self.createVEMap(triangles)
        adj = self.createNeighboorTable(triangle_num, edge_to_tri)

        visited = [False] * triangle_num
        submeshes = []
        print('[INFO][MeshSplitter::splitMesh]')
        print('\t start search connected component...')
        for i in trange(triangle_num):
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

    def splitMeshFile(self, mesh_file_path: str) -> List[o3d.geometry.TriangleMesh]:
        if not self.loadMeshFile(mesh_file_path):
            print('[ERROR][MeshSplitter::splitMeshFile]')
            print('\t loadMeshFile failed!')
            return []

        return self.splitMesh()
