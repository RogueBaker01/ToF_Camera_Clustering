import numpy as np
import cv2
import matplotlib.pyplot as plt

x = np.loadtxt("Datos/array_x1.txt")
y = np.loadtxt("Datos/array_y1.txt")
z = np.loadtxt("Datos/array_z1.txt")

# Normalizar los valores de x, y para asignarlos a una imagen 2D
x_min, x_max = np.min(x), np.max(x)
y_min, y_max = np.min(y), np.max(y)

# Convertir coordenadas x, y a índices de una imagen 2D con clip para evitar desbordamientos
x_img = np.clip(((x - x_min) / (x_max - x_min) * 255), 0, 255).astype(np.uint8)
y_img = np.clip(((y - y_min) / (y_max - y_min) * 255), 0, 255).astype(np.uint8)

# Crear una imagen basada en la profundidad (z) promediando valores si hay solapamiento
depth_image = np.zeros((256, 256), dtype=np.float32)
count = np.zeros((256, 256), dtype=np.int32)

for xi, yi, zi in zip(x_img, y_img, z):
    depth_image[yi, xi] += zi
    count[yi, xi] += 1

# Manejar divisiones por cero y normalizar
depth_image = np.divide(depth_image, count, where=count!=0)
z_min, z_max = np.nanmin(depth_image), np.nanmax(depth_image)
depth_image = 255 * (depth_image - z_min) / (z_max - z_min)
depth_image = np.nan_to_num(depth_image, nan=0).astype(np.uint8)

# Aplicar desenfoque gaussiano para reducir ruido
blurred = cv2.GaussianBlur(depth_image, (5, 5), 0)

# Aplicar umbralización de Otsu
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Eliminar ruido con morfología
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# Crear fondo seguro
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# Transformada de distancia para primer plano seguro
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.3 * dist_transform.max(), 255, 0)

sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)

# Crear marcadores para Watershed
_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

# Aplicar Watershed
depth_bgr = cv2.cvtColor(depth_image, cv2.COLOR_GRAY2BGR)
markers = cv2.watershed(depth_bgr, markers)
depth_bgr[markers == -1] = [255, 0, 0]

# Visualizar resultados
cv2.imwrite("depth_image.png", depth_image)
cv2.imwrite("watershed.png", depth_bgr)
