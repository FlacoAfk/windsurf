"""
Sistema de logging mejorado para Windsurf Reset Tool.
Registra todas las operaciones con timestamps y niveles de severidad.
"""
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler

console = Console()


class EnhancedLogger:
    """Logger mejorado con soporte para archivos y consola."""
    
    def __init__(self, name: str = "WindsurfReset", log_dir: Optional[Path] = None):
        """
        Inicializa el logger.
        
        Args:
            name: Nombre del logger
            log_dir: Directorio para guardar logs (opcional)
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Limpiar handlers existentes
        self.logger.handlers.clear()
        
        # Handler para consola (Rich)
        console_handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            show_time=False,
            show_path=False
        )
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter("%(message)s")
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # Handler para archivo (si se especifica directorio)
        if log_dir:
            log_dir = Path(log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"windsurf_reset_{timestamp}.log"
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
            
            self.log_file = log_file
        else:
            self.log_file = None
    
    def debug(self, message: str):
        """Log mensaje de debug."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log mensaje informativo."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log mensaje de advertencia."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log mensaje de error."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log mensaje crítico."""
        self.logger.critical(message)
    
    def log_operation(self, operation: str, status: str, details: str = ""):
        """
        Registra una operación con su estado.
        
        Args:
            operation: Nombre de la operación
            status: Estado (success, failed, warning)
            details: Detalles adicionales
        """
        emoji_map = {
            'success': '✅',
            'failed': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }
        
        emoji = emoji_map.get(status.lower(), '•')
        message = f"{emoji} {operation}"
        
        if details:
            message += f" - {details}"
        
        if status.lower() == 'success':
            self.info(message)
        elif status.lower() == 'failed':
            self.error(message)
        elif status.lower() == 'warning':
            self.warning(message)
        else:
            self.info(message)
    
    def log_file_operation(self, file_path: Path, operation: str, success: bool):
        """
        Registra operación sobre un archivo.
        
        Args:
            file_path: Ruta del archivo
            operation: Tipo de operación (delete, create, backup, etc.)
            success: Si fue exitosa
        """
        status = 'success' if success else 'failed'
        self.log_operation(
            f"{operation.capitalize()} file",
            status,
            str(file_path.name)
        )
    
    def log_summary(self, total: int, successful: int, failed: int):
        """
        Registra un resumen de operaciones.
        
        Args:
            total: Total de operaciones
            successful: Operaciones exitosas
            failed: Operaciones fallidas
        """
        self.info("="*60)
        self.info(f"📊 RESUMEN DE OPERACIONES:")
        self.info(f"   Total: {total}")
        self.info(f"   ✅ Exitosas: {successful}")
        self.info(f"   ❌ Fallidas: {failed}")
        self.info("="*60)
    
    def get_log_file_path(self) -> Optional[Path]:
        """Retorna la ruta del archivo de log si existe."""
        return self.log_file


# Instancia global para facilitar el uso
_global_logger: Optional[EnhancedLogger] = None


def get_logger(log_dir: Optional[Path] = None) -> EnhancedLogger:
    """
    Obtiene la instancia global del logger.
    
    Args:
        log_dir: Directorio para logs (solo en primera llamada)
    
    Returns:
        Instancia del logger
    """
    global _global_logger
    
    if _global_logger is None:
        _global_logger = EnhancedLogger(log_dir=log_dir)
    
    return _global_logger


# Ejemplo de uso
if __name__ == "__main__":
    # Crear logger con archivo
    log_dir = Path.home() / "Desktop" / "windsurf" / "logs"
    logger = get_logger(log_dir)
    
    # Ejemplos de uso
    logger.info("Iniciando Windsurf Reset Tool")
    logger.log_operation("Detectar rutas", "success", "Rutas encontradas correctamente")
    logger.log_operation("Cerrar Windsurf", "warning", "Proceso no encontrado")
    logger.log_operation("Eliminar cache", "failed", "Sin permisos")
    
    logger.log_file_operation(Path("test.json"), "delete", True)
    logger.log_file_operation(Path("backup.json"), "create", True)
    
    logger.log_summary(total=10, successful=8, failed=2)
    
    if logger.get_log_file_path():
        console.print(f"\n[green]Log guardado en: {logger.get_log_file_path()}[/green]")
