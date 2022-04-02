import numpy as np
import os
import open3d

# vis = open3d.visualization.Visualizer()
# vis.create_window()
 
base_path = r'tools/velodyne_points/data'
files = os.listdir(base_path)
files.sort(key=lambda x: int(x.split('.')[0]))

for file in files:
    #获取文件所属目录
    # print(root)
    #获取文件路径
    points = np.loadtxt(os.path.join(base_path,file), dtype=np.float32)
    points = points.reshape(-1, 4)
    
    # print(os.path.join(base_path, (os.path.splitext(file)[0] + '.npy')))
    
    points[:, 3] = 0 
    np.save(os.path.join(base_path, os.path.splitext(file)[0]), points) 
    
    # pts = open3d.geometry.PointCloud()
    # pts.points = open3d.utility.Vector3dVector(points[:, :3])
    # vis.add_geometry(pts)
    # # vis.update_geometry(source)
    # vis.poll_events()
    # vis.update_renderer()
    # vis.clear_geometries()
        