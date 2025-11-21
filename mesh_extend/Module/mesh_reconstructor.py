import os
import open3d as o3d
from tqdm import tqdm
from typing import Union, Optional

from wn_nc.Module.wnnc_reconstructor import WNNCReconstructor

from mesh_extend.Method.io import saveXYZ
from mesh_extend.Method.path import createFileFolder
from mesh_extend.Module.mesh_loader import MeshLoader


class MeshReconstructor(MeshLoader):
    def __init__(self, mesh_file_path: Optional[str] = None) -> None:
        MeshLoader.__init__(self, mesh_file_path)
        return

    def reconMesh(self) -> Union[o3d.geometry.TriangleMesh, None]:
        if not self.isValid():
            print('[ERROR][MeshReconstructor::reconMesh]')
            print('\t mesh not exist! please load mesh first')
            return None

        self.mesh.compute_vertex_normals()

        pcd = o3d.geometry.PointCloud()
        pcd.points = self.mesh.vertices
        pcd.normals = self.mesh.vertex_normals

        saveXYZ(pcd, './output/tmp.xyz')
        WNNCReconstructor.reconstructSurface('./output/tmp.xyz', './output/tmp.ply', use_gpu=True, overwrite=True)

        recon_mesh = o3d.io.read_triangle_mesh('./output/tmp.ply')
        return recon_mesh

        recon_success = False
        while not recon_success:
            try:
                recon_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                    pcd, 
                    depth=10  # 控制重建的精细度，值越大越精细
                )
                recon_success = True
            except:
                pass

        recon_mesh.compute_vertex_normals()

        return recon_mesh

    def reconMeshFile(self, mesh_file_path: str) -> Union[o3d.geometry.TriangleMesh, None]:
        if not self.loadMeshFile(mesh_file_path):
            print('[ERROR][MeshReconstructor::reconMeshFile]')
            print('\t loadMeshFile failed!')
            return None

        return self.reconMesh()

    def reconMeshFolder(self, mesh_folder_path: str) -> dict:
        if not os.path.exists(mesh_folder_path):
            print('[ERROR][MeshReconstructor::reconMeshFolder]')
            print('\t mesh folder not exist!')
            print('\t mesh_folder_path:', mesh_folder_path)

        recon_mesh_dict = {}
        mesh_filename_list = os.listdir(mesh_folder_path)

        print('[INFO][MeshReconstructor::reconMeshFolder]')
        print('\t start recon mesh folder...')
        for mesh_filename in tqdm(mesh_filename_list):
            if mesh_filename.split('.')[-1] not in ['ply', 'obj']:
                continue

            mesh_file_path = mesh_folder_path + mesh_filename

            recon_mesh = self.reconMeshFile(mesh_file_path)

            recon_mesh_dict[mesh_filename] = recon_mesh

        return recon_mesh_dict

    def saveReconMesh(self, recon_mesh: o3d.geometry.TriangleMesh, save_mesh_file_path: str) -> bool:
        createFileFolder(save_mesh_file_path)

        o3d.io.write_triangle_mesh(save_mesh_file_path, recon_mesh, write_ascii=True)
        return True

    def saveReconMeshDict(self, mesh_dict: dict, save_mesh_folder_path: str) -> bool:
        os.makedirs(save_mesh_folder_path, exist_ok=True)

        for filename, mesh in mesh_dict.items():
            curr_save_mesh_file_path = save_mesh_folder_path + filename
            o3d.io.write_triangle_mesh(curr_save_mesh_file_path, mesh, write_ascii=True)

        return True
