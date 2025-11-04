"""
Simulación de reseteo - Muestra exactamente qué hará el script SIN hacer cambios reales.
Este es un modo "dry-run" completamente seguro.
"""
import json
import os
import platform
import uuid
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

def get_windsurf_paths():
    """Obtiene las rutas de Windsurf."""
    system = platform.system()
    paths = {
        "Windows": Path(os.getenv("APPDATA", "")),
        "Darwin": Path.home() / "Library" / "Application Support",
        "Linux": Path.home() / ".config",
    }
    
    base_path = paths.get(system) / "Windsurf"
    storage_file = base_path / "User" / "globalStorage" / "storage.json"
    
    return base_path, storage_file

def simulate_clean_files(base_path):
    """Simula la limpieza de archivos."""
    console.print("\n[bold cyan]═══ PASO 1: LIMPIEZA DE ARCHIVOS ═══[/bold cyan]\n")
    
    paths_to_clean = [
        base_path / "Cookies",
        base_path / "Cookies-journal",
        base_path / "Network Persistent State",
        base_path / "Cache",
        base_path / "CachedData",
        base_path / "Code Cache",
        base_path / "GPUCache",
        base_path / "Session Storage",
        base_path / "Local Storage",
        base_path / "IndexedDB",
        base_path / "User" / "globalStorage" / "codeium.windsurf",
        base_path / "User" / "workspaceStorage",
        base_path / "logs",
    ]
    
    table = Table(title="Archivos/Directorios a Eliminar")
    table.add_column("Acción", style="red bold")
    table.add_column("Ruta", style="white")
    table.add_column("Estado Actual", style="cyan")
    table.add_column("Efecto", style="yellow")
    
    will_delete = 0
    total_size = 0
    
    for path in paths_to_clean:
        if path.exists():
            tipo = "🗑️  ELIMINAR"
            estado = "✅ Existe"
            
            try:
                if path.is_file():
                    size = path.stat().st_size
                    total_size += size
                elif path.is_dir():
                    size = get_dir_size(path)
                    total_size += size
                efecto = f"Liberará {format_size(size)}"
            except:
                efecto = "Liberará espacio"
            
            table.add_row(tipo, str(path.name), estado, efecto)
            will_delete += 1
        else:
            table.add_row("⏭️  OMITIR", str(path.name), "❌ No existe", "Sin efecto")
    
    console.print(table)
    
    console.print(f"\n[yellow]📊 Resumen de limpieza:[/yellow]")
    console.print(f"   • Se eliminarán: [red bold]{will_delete}[/red bold] archivos/directorios")
    console.print(f"   • Espacio a liberar: [yellow bold]{format_size(total_size)}[/yellow bold]")
    console.print(f"   • Se omitirán: [cyan]{len(paths_to_clean) - will_delete}[/cyan] (no existen)")
    
    return will_delete > 0

def simulate_storage_json(storage_file):
    """Simula los cambios en storage.json."""
    console.print("\n[bold cyan]═══ PASO 2: MODIFICACIÓN DE storage.json ═══[/bold cyan]\n")
    
    if not storage_file.exists():
        console.print("[yellow]⚠️  storage.json no existe, será creado[/yellow]\n")
        console.print("[cyan]Se creará con:[/cyan]")
        new_ids = {
            "telemetry.machineId": os.urandom(32).hex(),
            "telemetry.macMachineId": os.urandom(32).hex(),
            "telemetry.devDeviceId": str(uuid.uuid4()),
        }
        
        table = Table(title="Nuevos IDs que se crearán")
        table.add_column("Clave", style="yellow")
        table.add_column("Valor", style="green")
        
        for key, value in new_ids.items():
            table.add_row(key, value)
        
        console.print(table)
        return True
    
    try:
        with open(storage_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        console.print(f"[green]✅ storage.json existe con {len(data)} claves[/green]\n")
        
        # Identificar claves que se eliminarán
        keys_to_remove = [
            k for k in data.keys() 
            if k.startswith(('telemetry', 'codeium', 'windsurf', 'auth', 'session'))
        ]
        
        if keys_to_remove:
            console.print(f"[red]🗑️  Se eliminarán {len(keys_to_remove)} claves:[/red]")
            
            table = Table(title="Claves a Eliminar")
            table.add_column("Clave", style="red")
            table.add_column("Valor Actual (truncado)", style="yellow")
            
            for key in keys_to_remove[:15]:  # Mostrar máximo 15
                value_str = str(data.get(key, ""))[:50]
                if len(str(data.get(key, ""))) > 50:
                    value_str += "..."
                table.add_row(key, value_str)
            
            if len(keys_to_remove) > 15:
                console.print(f"\n[yellow]... y {len(keys_to_remove) - 15} claves más[/yellow]")
            
            console.print(table)
        else:
            console.print("[yellow]⚠️  No se encontraron claves para eliminar[/yellow]")
        
        # Mostrar nuevos IDs que se agregarán
        console.print(f"\n[green]➕ Se agregarán 3 nuevos IDs:[/green]")
        
        new_ids = {
            "telemetry.machineId": os.urandom(32).hex(),
            "telemetry.macMachineId": os.urandom(32).hex(),
            "telemetry.devDeviceId": str(uuid.uuid4()),
        }
        
        table = Table(title="Nuevos IDs que se generarán")
        table.add_column("Clave", style="yellow")
        table.add_column("Valor (ejemplo)", style="green")
        table.add_column("Tipo", style="cyan")
        
        table.add_row("telemetry.machineId", new_ids["telemetry.machineId"], "64 chars hex")
        table.add_row("telemetry.macMachineId", new_ids["telemetry.macMachineId"], "64 chars hex")
        table.add_row("telemetry.devDeviceId", new_ids["telemetry.devDeviceId"], "UUID v4")
        
        console.print(table)
        
        # Mostrar resumen de cambios
        console.print(f"\n[yellow]📊 Resumen de cambios en storage.json:[/yellow]")
        console.print(f"   • Claves eliminadas: [red bold]{len(keys_to_remove)}[/red bold]")
        console.print(f"   • Claves agregadas: [green bold]3[/green bold]")
        console.print(f"   • Claves sin cambios: [cyan]{len(data) - len(keys_to_remove)}[/cyan]")
        console.print(f"   • Total final: [yellow bold]{len(data) - len(keys_to_remove) + 3}[/yellow bold] claves")
        
        return True
        
    except json.JSONDecodeError:
        console.print("[yellow]⚠️  storage.json tiene formato inválido, será recreado[/yellow]")
        return True
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        return False

def check_windsurf_processes():
    """Verifica si hay procesos de Windsurf."""
    console.print("\n[bold cyan]═══ PASO 0: VERIFICACIÓN DE PROCESOS ═══[/bold cyan]\n")
    
    try:
        import psutil
        
        process_names = ["Windsurf.exe", "windsurf", "Windsurf", "windsurf.exe"]
        windsurf_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if proc.info['name'] in process_names:
                    windsurf_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if windsurf_processes:
            console.print(f"[yellow]⚠️  ADVERTENCIA: Windsurf está en ejecución[/yellow]")
            
            table = Table(title="Procesos Detectados")
            table.add_column("PID", style="cyan")
            table.add_column("Nombre", style="white")
            table.add_column("Memoria", style="yellow")
            table.add_column("Acción", style="red")
            
            for proc in windsurf_processes:
                try:
                    mem = proc.info['memory_info'].rss
                    table.add_row(
                        str(proc.info['pid']),
                        proc.info['name'],
                        format_size(mem),
                        "🔴 Será cerrado"
                    )
                except:
                    pass
            
            console.print(table)
            console.print("\n[red]⚠️  El script cerrará estos procesos automáticamente[/red]")
            console.print("[yellow]   (o te preguntará si quieres cerrarlos)[/yellow]")
        else:
            console.print("[green]✅ Windsurf no está en ejecución[/green]")
            console.print("[green]   No se necesita cerrar ningún proceso[/green]")
        
        return True
        
    except ImportError:
        console.print("[yellow]⚠️  psutil no disponible[/yellow]")
        console.print("[yellow]   No se puede verificar si Windsurf está ejecutándose[/yellow]")
        console.print("[cyan]   Instala con: pip install psutil[/cyan]")
        return True

def simulate_backup(storage_file):
    """Simula la creación de backup."""
    console.print("\n[bold cyan]═══ BACKUP ═══[/bold cyan]\n")
    
    if storage_file.exists():
        from datetime import datetime
        backup_name = f"storage.json.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = storage_file.parent / backup_name
        
        console.print("[cyan]Si aceptas crear backup:[/cyan]")
        console.print(f"   📁 Se creará: [yellow]{backup_path}[/yellow]")
        
        try:
            size = storage_file.stat().st_size
            console.print(f"   📦 Tamaño: [cyan]{format_size(size)}[/cyan]")
        except:
            pass
        
        console.print("\n[green]✅ El backup te permitirá restaurar si algo sale mal[/green]")
    else:
        console.print("[yellow]⚠️  storage.json no existe, no hay nada para respaldar[/yellow]")

def get_dir_size(path):
    """Calcula el tamaño de un directorio."""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_dir_size(entry.path)
    except:
        pass
    return total

def format_size(size):
    """Formatea el tamaño en bytes."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def main():
    """Función principal de simulación."""
    console.clear()
    
    console.print(Panel(
        Text(
            "SIMULACIÓN DE RESETEO\n\n"
            "Este script muestra EXACTAMENTE qué hará el reseteo\n"
            "SIN hacer ningún cambio real.\n\n"
            "Es completamente seguro.",
            justify="center"
        ),
        title="🎭 MODO DRY-RUN",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    # Obtener rutas
    base_path, storage_file = get_windsurf_paths()
    
    console.print(f"\n[cyan]📍 Ruta de Windsurf:[/cyan] {base_path}")
    console.print(f"[cyan]📄 Archivo storage.json:[/cyan] {storage_file}\n")
    
    # Simular verificación de procesos
    check_windsurf_processes()
    
    # Simular backup
    simulate_backup(storage_file)
    
    # Simular limpieza de archivos
    will_clean = simulate_clean_files(base_path)
    
    # Simular modificación de storage.json
    will_modify = simulate_storage_json(storage_file)
    
    # Resumen final
    console.print("\n" + "="*60)
    console.print("[bold cyan]═══ RESUMEN FINAL DE LA SIMULACIÓN ═══[/bold cyan]\n")
    
    summary_table = Table(title="Qué Hará El Script Real")
    summary_table.add_column("Paso", style="cyan")
    summary_table.add_column("Acción", style="white")
    summary_table.add_column("Impacto", style="yellow")
    
    summary_table.add_row(
        "1️⃣", 
        "Verificar si Windsurf está ejecutándose",
        "Cerrará procesos si es necesario"
    )
    summary_table.add_row(
        "2️⃣",
        "Crear backup de storage.json",
        "Protección contra errores"
    )
    summary_table.add_row(
        "3️⃣",
        "Eliminar archivos de sesión/cache",
        f"{'Liberará espacio' if will_clean else 'Sin archivos para limpiar'}"
    )
    summary_table.add_row(
        "4️⃣",
        "Limpiar claves de auth en storage.json",
        "Forzará nueva API key"
    )
    summary_table.add_row(
        "5️⃣",
        "Generar nuevos IDs de dispositivo",
        "3 nuevos identificadores únicos"
    )
    summary_table.add_row(
        "6️⃣",
        "Guardar cambios en storage.json",
        "Cambios permanentes"
    )
    
    console.print(summary_table)
    
    console.print("\n[yellow]⚠️  IMPORTANTE:[/yellow]")
    console.print("   • Los cambios son [red bold]PERMANENTES[/red bold] (a menos que uses el backup)")
    console.print("   • Debes [yellow bold]REINICIAR WINDSURF[/yellow bold] después del reseteo")
    console.print("   • La nueva API key se generará al [cyan]iniciar sesión de nuevo[/cyan]")
    
    console.print("\n" + "="*60)
    console.print(Panel(
        Text(
            "Esta fue solo una SIMULACIÓN.\n\n"
            "Para ejecutar el reseteo REAL, ejecuta:\n"
            "python windsurf_reset.py\n\n"
            "O usa el script batch:\n"
            "run_reset.bat",
            justify="center"
        ),
        title="[bold green]✅ SIMULACIÓN COMPLETADA[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Simulación cancelada[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
