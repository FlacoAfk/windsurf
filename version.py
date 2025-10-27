"""
Sistema de versionamiento automático para Windsurf Reset Tool
"""

__version__ = "2.0.0"
__author__ = "Windsurf Reset Tool Team"
__license__ = "MIT"
__copyright__ = "2024"

# Historial de versiones
VERSION_HISTORY = {
    "2.0.0": {
        "date": "2024-10-26",
        "changes": [
            "Reseteo completo de autenticación y API keys",
            "Limpieza profunda de 15+ tipos de archivos",
            "Detección y cierre automático de procesos Windsurf",
            "Suite completa de pruebas (test_script.py)",
            "Simulación dry-run (simulate_reset.py)",
            "Verificación post-reseteo (verify_changes.py)",
            "Documentación exhaustiva en español",
            "Scripts de inicio rápido para Windows",
            "Backups automáticos con timestamp",
            "Soporte multiplataforma (Windows, macOS, Linux)"
        ],
        "type": "major"
    },
    "1.0.0": {
        "date": "2024-10-25",
        "changes": [
            "Versión inicial",
            "Reseteo básico de IDs de telemetría",
            "Interfaz con Rich",
            "Backups con timestamp"
        ],
        "type": "initial"
    }
}

def get_version():
    """Obtiene la versión actual."""
    return __version__

def get_version_info():
    """Obtiene información detallada de la versión."""
    return {
        "version": __version__,
        "author": __author__,
        "license": __license__,
        "copyright": __copyright__
    }

def print_version():
    """Imprime información de la versión."""
    print(f"Windsurf Reset Tool v{__version__}")
    print(f"Copyright {__copyright__} {__author__}")
    print(f"License: {__license__}")
    print("\nRecent changes:")
    latest = list(VERSION_HISTORY.keys())[0]
    for change in VERSION_HISTORY[latest]["changes"][:5]:
        print(f"  • {change}")

if __name__ == "__main__":
    print_version()
