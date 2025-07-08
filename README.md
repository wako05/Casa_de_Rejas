# Casa de Rejas

Sistema de inventario y ventas para Casa de Rejas.

## Requisitos

- Python 3.8 o superior

## Instalación

1. Clona este repositorio en el otro PC:
   ```
   git clone https://github.com/wako05/Casa_de_Rejas.git
   cd Casa_de_Rejas
   ```

2. Instala las dependencias (asegúrate de tener Python 3.8 o superior instalado):
   ```
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```
   streamlit run ui.py
   ```

   O si prefieres usar el ejecutable (si está disponible):
   ```
   # En Windows, desde la carpeta dist:
   dist\run_app.exe
   ```

## Despliegue en Streamlit Cloud

Puedes ejecutar esta aplicación gratis en [Streamlit Cloud](https://streamlit.io/cloud):

1. Sube este repositorio a GitHub (ya lo tienes).
2. Ingresa a [https://streamlit.io/cloud](https://streamlit.io/cloud) y haz login con tu cuenta de GitHub.
3. Haz clic en "New app" y selecciona tu repositorio y la rama (por ejemplo, `main`).
4. En "Main file path" escribe:  
   ```
   ui.py
   ```
5. Haz clic en "Deploy".

La aplicación se desplegará y recibirás una URL pública para acceder desde cualquier PC o celular.

**Notas:**
- Los archivos generados (como la base de datos y los Excel) estarán en el entorno de Streamlit Cloud, no en tu PC.
- Si quieres conservar los datos, descarga los archivos exportados desde la interfaz antes de reiniciar la app.

## Notas

- La base de datos SQLite se crea automáticamente.
- Puedes exportar los datos a Excel desde la interfaz.
- Funciona en PC y navegadores móviles (la experiencia móvil puede ser limitada).

## ¿Cómo subir tus cambios a tu repositorio de GitHub?

1. **Guarda todos los archivos modificados en tu proyecto.**

2. **Abre una terminal en la carpeta de tu proyecto.**

3. **Agrega los archivos modificados al área de preparación:**
   ```
   git add .
   ```

4. **Haz un commit con un mensaje descriptivo:**
   ```
   git commit -m "Describe brevemente los cambios realizados"
   ```

5. **Sube los cambios a tu repositorio remoto en GitHub:**
   ```
   git push
   ```

6. **¡Listo! Tus cambios estarán disponibles en GitHub.**
