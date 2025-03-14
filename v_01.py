import numpy as np
import matplotlib.pyplot as plt

def make_m(file_d, file_x, file_y, n_row = 132, n_col = 176): # Funcion para crear la matriz.
    # Abrir los archivos en modo lectura, leo los valores eliminando los espacios en blanco y los convierto a float.
    with open(file_d, 'r') as fd, open(file_x, 'r') as fx, open(file_y, 'r') as fy:
        values = [float(line.strip()) for line in fd] # Valores distancia.
        x_coords = [float(line.strip()) for line in fx] # Valores eje x.
        y_coords = [float(line.strip()) for line in fy] # Valores eje y.
    
    # Creo la matriz con valores faltantes (.nan).
    matrix = np.full((n_row, n_col), np.nan) 
    
    # Convertir x_coords y y_coords en arreglos NumPy.
    # Resto el valor minimo para que el rango empiece en 0.
    # Divido entre la diferencia del maximo y el minimo para tener valores en el rango [0, 1].
    # Ajusto el tamaño de la matriz al multiplicar por (n_col - 1) y (n_row - 1), utilizo .astype(int) para obtener indices validos.
    # Redondeo.
    x_indices = np.round((np.array(x_coords) - min(x_coords)) / (max(x_coords) - min(x_coords)) * (n_col - 1)).astype(int)
    y_indices = np.round((np.array(y_coords) - min(y_coords)) / (max(y_coords) - min(y_coords)) * (n_row - 1)).astype(int)
    
    # Confirmo que los indices esten dentro del rango y le asigno el valor de la distancia, realmente no es necesario el if ya que todos los archivos siempre tienen el mismo numero de datos.
    for i in range(len(values)):
        if 0 <= y_indices[i] < n_row and 0 <= x_indices[i] < n_col: 
            matrix[y_indices[i], x_indices[i]] = values[i]
    
    return matrix

def show_m(matrix): # Funcion para imprimir la matriz.
    plt.figure(figsize=(10, 7))
    plt.imshow(matrix[::-1], cmap='viridis', interpolation='nearest') # [::-1] para invertir la matriz.
    plt.colorbar(label='distancias')
    plt.title('No se :D')
    plt.show()

file_d = 'Datos/array_x1.txt' # Archivo distancias.
file_x = 'Datos/array_y1.txt' # Archivo puntos eje x.
file_y = 'Datos/array_z1.txt' # Archivo puntos eje y.

matrix_d = make_m(file_d, file_x, file_y)
show_m(matrix_d)