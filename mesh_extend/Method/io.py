import numpy as np
import open3d as o3d

from mesh_extend.Method.path import createFileFolder

def saveXYZ(pcd: o3d.geometry.PointCloud, save_xyz_file_path: str) -> bool:
    points = np.asarray(pcd.points)

    createFileFolder(save_xyz_file_path)

    normals = np.asarray(pcd.normals)
    if normals.shape[0] == points.shape[0]:
        data = np.hstack([points, normals])
        np.savetxt(save_xyz_file_path, data, fmt="%.6f %.6f %.6f %.6f %.6f %.6f")
        return True

    np.savetxt(save_xyz_file_path, points, fmt="%.6f %.6f %.6f")

    return True
