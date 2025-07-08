import subprocess
import sys
import os

# Obtiene el directorio donde se encuentra este script (run_app.py).
# Esto es crucial para que PyInstaller encuentre correctamente ui.py.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta a tu archivo ui.py, relativa a run_app.py.
ui_path = os.path.join(script_dir, "ui.py")

# Comando para ejecutar Streamlit.
# Usamos 'python -m streamlit' para asegurar que se use la versión correcta
# de Streamlit cuando se ejecuta desde un entorno empaquetado.
# '--server.port 0' hace que Streamlit elija un puerto disponible automáticamente.
# '--browser.gatherUsageStats false' deshabilita las estadísticas de uso.
command = [
    sys.executable, "-m", "streamlit", "run", ui_path,
    "--server.port", "580",
    "--browser.gatherUsageStats", "false"
]

print(f"Lanzando Streamlit con el comando: {' '.join(command)}")

try:
    # Inicia el proceso de Streamlit.
    # Usamos subprocess.Popen para ejecutarlo en segundo plano y no bloquear
    # el script actual. Esto también permite que la ventana de la consola
    # (si no se usa --windowed) se cierre después del lanzamiento.
    subprocess.Popen(command)
except Exception as e:
    print(f"Error al lanzar Streamlit: {e}")
    # En una aplicación real, podrías querer registrar esto o mostrar
    # un cuadro de mensaje. Para una aplicación de PyInstaller,
    # un simple 'print' podría no ser visible si se usa --windowed.

