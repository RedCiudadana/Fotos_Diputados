import pandas as pd
import requests
import os
import re
import time
from PIL import Image
from io import BytesIO

# Cargar el archivo Excel
file_path = 'C:/Users/josem/Documents/GitHub/Fotos_Diputados/diputados_perfiles.xlsx'
df = pd.read_excel(file_path)

# Crear una carpeta para las imágenes
output_folder = 'imagenes_diputados'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Función para convertir el nombre en slug
def slugify(name):
    name = name.lower()
    name = re.sub(r'\s+', '-', name)
    name = re.sub(r'[^a-z0-9\-]', '', name)
    return name

# Descargar cada imagen con verificación de tipo de contenido
for index, row in df.iterrows():
    image_url = row['Imagen URL']  # Cambia al nombre exacto de la columna
    nombre = row['Nombre']  # Cambia al nombre exacto de la columna
    if pd.notnull(image_url):
        slug_name = slugify(nombre)
        file_name = os.path.join(output_folder, f"{slug_name}.jpg")
        
        for attempt in range(3):  # Intentar hasta 3 veces
            try:
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()  # Verificar si la descarga fue exitosa
                
                # Verificar si el tipo de contenido es una imagen
                if 'image' in response.headers.get('Content-Type', ''):
                    image = Image.open(BytesIO(response.content))
                    image.verify()  # Verificar que el contenido sea una imagen
                    # Guardar la imagen si es válida
                    with open(file_name, 'wb') as file:
                        file.write(response.content)
                    
                    print(f"Descargado correctamente: {nombre} como {slug_name}.jpg")
                    break
                else:
                    print(f"{nombre} no es una imagen. Tipo de contenido recibido: {response.headers.get('Content-Type')}")
                    break
            except (requests.exceptions.RequestException, Image.UnidentifiedImageError) as e:
                print(f"Error en la descarga de {nombre}: {e}")
                time.sleep(2)  # Espera antes de reintentar
