"""
Script para verificar y cerrar procesos de Windsurf antes del reseteo.
"""
import psutil
import platform
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def get_windsurf_processes():
    """Encuentra todos los procesos de Windsurf en ejecución."""
    windsurf_processes = []
    process_names = ["Windsurf.exe", "windsurf", "Windsurf", "windsurf.exe"]
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] in process_names:
                windsurf_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return windsurf_processes

def kill_windsurf_processes():
    """Intenta cerrar todos los procesos de Windsurf."""
    processes = get_windsurf_processes()
    
    if not processes:
        console.print("[success]No hay procesos de Windsurf en ejecución.[/success]")
        return True
    
    console.print(f"[warning]Se encontraron {len(processes)} proceso(s) de Windsurf en ejecución.[/warning]")
    
    for proc in processes:
        try:
            console.print(f"[info]Cerrando proceso: {proc.info['name']} (PID: {proc.info['pid']})[/info]")
            proc.terminate()
            proc.wait(timeout=5)
            console.print(f"[success]Proceso {proc.info['pid']} cerrado correctamente.[/success]")
        except psutil.TimeoutExpired:
            console.print(f"[warning]Forzando cierre del proceso {proc.info['pid']}...[/warning]")
            proc.kill()
        except Exception as e:
            console.print(f"[error]Error al cerrar proceso {proc.info['pid']}: {str(e)}[/error]")
            return False
    
    return True

def main():
    """Función principal."""
    console.print(Panel(
        Text("Verificador de Procesos de Windsurf", justify="center"),
        title="🔍 Check Windsurf",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    processes = get_windsurf_processes()
    
    if processes:
        console.print(f"\n[warning]⚠️  Se encontraron {len(processes)} proceso(s) de Windsurf en ejecución:[/warning]\n")
        for proc in processes:
            console.print(f"  • PID: {proc.info['pid']} - Nombre: {proc.info['name']}")
        
        console.print("\n[info]Recomendación: Cierra Windsurf manualmente antes de ejecutar el reseteo.[/info]")
        console.print("[prompt]¿Quieres intentar cerrar estos procesos automáticamente? (s/n): [/prompt]", end="")
        
        choice = input().lower()
        if choice == 's' or choice == 'y':
            if kill_windsurf_processes():
                console.print("\n[success]✅ Todos los procesos de Windsurf han sido cerrados.[/success]")
                console.print("[info]Ahora puedes ejecutar el script de reseteo.[/info]")
            else:
                console.print("\n[error]❌ No se pudieron cerrar algunos procesos.[/error]")
                console.print("[warning]Cierra Windsurf manualmente desde el Task Manager.[/warning]")
        else:
            console.print("\n[info]Por favor, cierra Windsurf manualmente antes de continuar.[/info]")
    else:
        console.print("\n[success]✅ No hay procesos de Windsurf en ejecución.[/success]")
        console.print("[info]Es seguro ejecutar el script de reseteo.[/info]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[warning]Operación cancelada por el usuario.[/warning]")
    except Exception as e:
        console.print(f"\n[error]Error: {str(e)}[/error]")
