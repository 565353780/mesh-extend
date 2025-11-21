from mesh_extend.Demo.mesh_splitter import demo as demo_split_mesh

if __name__ == "__main__":
    demo_split_mesh()
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
