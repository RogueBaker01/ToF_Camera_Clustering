import numpy as np
import open3d as o3d

x = np.asarray("/Datos/array_x1.txt")
y = np.asarray("Datos/array_y1.txt")
z = np.asarray("Datos/array_z1.txt")

xyz = x*y*z

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)

o3d.io.write_point_cloud("nube_puntos.pcd", pcd)

print("Nube de puntos guardada como 'nube_puntos.pcd'")
