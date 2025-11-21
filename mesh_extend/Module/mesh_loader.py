import os
import numpy as np
import open3d as o3d
from typing import Optional


class MeshLoader(object):
    def __init__(self, mesh_file_path: Optional[str] = None) -> None:
        self.mesh: Optional[o3d.geometry.TriangleMesh] = None

        if mesh_file_path is not None:
            self.loadMeshFile(mesh_file_path)
        return

    def loadMeshFile(self, mesh_file_path: str) -> bool:
        if not os.path.exists(mesh_file_path):
            print('[ERROR][MeshLoader::loadMeshFile]')
            print('\t mesh file not exist!')
            print('\t mesh_file_path:', mesh_file_path)
            return False

        self.mesh = o3d.io.read_triangle_mesh(mesh_file_path)
        return True

    def isValid(self) -> bool:
        if self.mesh is None:
            return False

        vertices = np.asarray(self.mesh.vertices)
        if vertices.shape[0] == 0:
            return False

        return True
