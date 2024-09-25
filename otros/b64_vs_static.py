import base64
import os

file_path = 'upload/example.txt'
with open(file_path, 'w') as f:
    f.write('Este es un archivo de prueba. ' * 1000)  

# Tamaño original del archivo
original_size = os.path.getsize(file_path)

# Leyendo el archivo y codificándolo en Base64
with open(file_path, 'rb') as f:
    encoded_content = base64.b64encode(f.read())

# Tamaño del archivo codificado en Base64
encoded_size = len(encoded_content)

# Calculando el aumento de tamaño en porcentaje
size_increase_percentage = ((encoded_size - original_size) / original_size) * 100

# original_size, encoded_size, size_increase_percentage

print(f'Tamaño original: {original_size} bytes')
print(f'Tamaño codificado: {encoded_size} bytes')
print(f'Incremento de tamaño: {size_increase_percentage}%')