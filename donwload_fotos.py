import os
import re
import time
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración de Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Crear una carpeta para las imágenes
output_folder = 'imagenes_diputados'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

import pandas as pd
import re

# Cargar el archivo Excel
file_path = './diputados_perfiles.xlsx'
df = pd.read_excel(file_path)

# Crear lista de nombres y URLs de imágenes en formato slug
def slugify(name):
    # Convertir a minúsculas y reemplazar caracteres acentuados
    name = name.lower()
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ü': 'u', 'ñ': 'n'
    }
    for accented_char, unaccented_char in replacements.items():
        name = name.replace(accented_char, unaccented_char)
    # Reemplazar espacios por guiones y eliminar caracteres especiales
    name = re.sub(r'\s+', '-', name)
    name = re.sub(r'[^a-z0-9\-]', '', name)
    return name

# Crear lista de diputados con nombres en slug y URLs
diputados = [
    {"nombre": row['Nombre'], "slug_nombre": slugify(row['Nombre']), "url": row['Imagen URL']}
    for index, row in df.iterrows() if pd.notnull(row['Imagen URL'])
]

# Descargar cada imagen utilizando Selenium
for diputado in diputados:
    nombre = diputado["nombre"]
    image_url = diputado["url"]
    slug_name = slugify(nombre)
    file_path = os.path.join(output_folder, f"{slug_name}.jpg")
    
    # Abrir la URL de la imagen en el navegador
    driver.get(image_url)
    
    # Espera breve para asegurarse de que la imagen se cargue
    time.sleep(2)
    
    # Capturar la pantalla y guardar la imagen
    driver.save_screenshot(file_path)
    print(f"Imagen guardada para {nombre} en {file_path}")

# Cerrar el navegador
driver.quit()
