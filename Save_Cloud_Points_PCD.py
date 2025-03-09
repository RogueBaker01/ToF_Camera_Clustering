import numpy as np
import open3d as o3d

x = np.loadtxt("Datos/array_x1.txt")
y = np.loadtxt("Datos/array_y1.txt")
z= np.loadtxt("Datos/array_z1.txt")

#Combina los arrays en una matriz
xyz = np.column_stack((x,y,z))

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)

o3d.io.write_point_cloud("nube_puntos.pcd", pcd)

print("Nube de puntos guardada como 'nube_puntos.pcd'")
