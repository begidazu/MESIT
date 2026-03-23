# app/config.py
# ============================================================================
# CONFIGURACIÓN CENTRALIZADA DE RUTAS
# ============================================================================
# Este módulo define el punto de referencia para todas las rutas relativas
# al proyecto. En producción, asegura que las rutas se resuelvan
# correctamente independientemente del directorio de trabajo.
# ============================================================================

import os
from pathlib import Path

# Obtener la ruta raíz del proyecto
# os.path.dirname(__file__) devuelve la ruta de la carpeta 'app/'
# Luego subimos un nivel (..) para obtener la raíz del proyecto
APP_DIR = Path(__file__).parent  # /app
PROJECT_ROOT = APP_DIR.parent     # raíz del proyecto

def get_project_root() -> Path:
    """
    Devuelve la ruta raíz del proyecto como un objeto Path.
    Esta función es robusta a cambios de directorio de trabajo.
    """
    return PROJECT_ROOT

def resolve_path(relative_path: str) -> str:
    """
    Convierte una ruta relativa al proyecto en una ruta absoluta.
    
    Args:
        relative_path (str): Ruta relativa al proyecto, ej: "results/opsa/Santander/eunis_santander.parquet"
    
    Returns:
        str: Ruta absoluta y normalizada
    
    Ejemplo:
        >>> resolve_path("results/opsa/Santander/eunis_santander.parquet")
        '/home/app/results/opsa/Santander/eunis_santander.parquet'
    """
    if not relative_path:
        return ""
    
    # Normalizar la ruta (cambiar barras, limpiar puntos)
    normalized = os.path.normpath(relative_path)
    
    # Construir la ruta absoluta
    absolute_path = PROJECT_ROOT / normalized
    
    return str(absolute_path)

def path_exists(relative_path: str) -> bool:
    """
    Verifica si una ruta (relativa al proyecto) existe.
    Útil para validar antes de intentar abrir archivos.
    """
    return (PROJECT_ROOT / relative_path).exists()
