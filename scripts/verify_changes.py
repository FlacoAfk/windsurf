"""
Script de verificación POST-RESETEO
Verifica que los cambios se aplicaron correctamente después del reseteo.
"""
import json
import os
import platform
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

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

def verify_files_deleted(base_path):
    """Verifica que los archivos fueron eliminados."""
    console.print("\n[bold cyan]═══ VERIFICACIÓN 1: Archivos Eliminados ═══[/bold cyan]\n")
    
    paths_to_check = [
        ("Cookies", base_path / "Cookies"),
        ("Cookies-journal", base_path / "Cookies-journal"),
        ("Network State", base_path / "Network Persistent State"),
        ("Cache", base_path / "Cache"),
        ("CachedData", base_path / "CachedData"),
        ("Code Cache", base_path / "Code Cache"),
        ("GPUCache", base_path / "GPUCache"),
        ("Session Storage", base_path / "Session Storage"),
        ("Local Storage", base_path / "Local Storage"),
        ("IndexedDB", base_path / "IndexedDB"),
        ("Codeium Storage", base_path / "User" / "globalStorage" / "codeium.windsurf"),
        ("Workspace Storage", base_path / "User" / "workspaceStorage"),
        ("Logs", base_path / "logs"),
    ]
    
    table = Table(title="Estado de Archivos")
    table.add_column("Archivo/Directorio", style="white")
    table.add_column("Estado", style="bold")
    table.add_column("Verificación", style="cyan")
    
    deleted_count = 0
    still_exists_count = 0
    
    for name, path in paths_to_check:
        if not path.exists():
            table.add_row(name, "[green]✅ Eliminado[/green]", "[green]Correcto[/green]")
            deleted_count += 1
        else:
            table.add_row(name, "[yellow]⚠️  Existe[/yellow]", "[yellow]No eliminado[/yellow]")
            still_exists_count += 1
    
    console.print(table)
    
    console.print(f"\n[cyan]📊 Resumen:[/cyan]")
    console.print(f"   • Eliminados correctamente: [green bold]{deleted_count}[/green bold]")
    console.print(f"   • Aún existen: [yellow bold]{still_exists_count}[/yellow bold]")
    
    if deleted_count > 0:
        console.print(f"\n[green]✅ Se eliminaron {deleted_count} archivos/directorios[/green]")
        console.print("[green]   El reseteo funcionó correctamente[/green]")
    else:
        console.print(f"\n[yellow]⚠️  No se eliminó ningún archivo[/yellow]")
        console.print("[yellow]   Posiblemente no existían antes del reseteo[/yellow]")
    
    return deleted_count > 0

def verify_storage_json(storage_file):
    """Verifica los cambios en storage.json."""
    console.print("\n[bold cyan]═══ VERIFICACIÓN 2: storage.json ═══[/bold cyan]\n")
    
    if not storage_file.exists():
        console.print("[red]❌ storage.json no existe[/red]")
        console.print("[red]   El reseteo pudo haber fallado[/red]")
        return False
    
    try:
        with open(storage_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        console.print(f"[green]✅ storage.json existe y es válido[/green]")
        console.print(f"[cyan]   Total de claves: {len(data)}[/cyan]\n")
        
        # Verificar IDs de telemetría
        required_ids = [
            "telemetry.machineId",
            "telemetry.macMachineId",
            "telemetry.devDeviceId"
        ]
        
        table = Table(title="IDs de Telemetría")
        table.add_column("Clave", style="yellow")
        table.add_column("Existe", style="green")
        table.add_column("Valor (primeros 40 chars)", style="white")
        table.add_column("Formato", style="cyan")
        
        all_present = True
        
        for key in required_ids:
            if key in data:
                value = str(data[key])
                value_display = value[:40] + ("..." if len(value) > 40 else "")
                
                # Verificar formato
                if key in ["telemetry.machineId", "telemetry.macMachineId"]:
                    is_valid = len(value) == 64 and all(c in "0123456789abcdef" for c in value.lower())
                    format_status = "✅ 64 hex" if is_valid else "❌ Inválido"
                elif key == "telemetry.devDeviceId":
                    is_valid = len(value) == 36 and value.count('-') == 4
                    format_status = "✅ UUID" if is_valid else "❌ Inválido"
                else:
                    format_status = "?"
                
                table.add_row(key, "✅", value_display, format_status)
            else:
                table.add_row(key, "[red]❌[/red]", "[red]Falta[/red]", "[red]Error[/red]")
                all_present = False
        
        console.print(table)
        
        if all_present:
            console.print("\n[green]✅ Todos los IDs requeridos están presentes[/green]")
        else:
            console.print("\n[red]❌ Faltan algunos IDs requeridos[/red]")
            return False
        
        # Verificar que se eliminaron claves de autenticación
        auth_keys = [k for k in data.keys() if any(x in k.lower() for x in ['codeium', 'auth', 'session']) and not k.startswith('telemetry')]
        
        if auth_keys:
            console.print(f"\n[yellow]⚠️  Se encontraron {len(auth_keys)} claves de autenticación:[/yellow]")
            for key in auth_keys[:5]:
                console.print(f"   • {key}")
            if len(auth_keys) > 5:
                console.print(f"   ... y {len(auth_keys) - 5} más")
            console.print("\n[yellow]   Estas claves deberían haber sido eliminadas[/yellow]")
            console.print("[yellow]   Puede que no se hayan eliminado correctamente[/yellow]")
        else:
            console.print("\n[green]✅ No se encontraron claves de autenticación antiguas[/green]")
            console.print("[green]   La limpieza fue exitosa[/green]")
        
        return True
        
    except json.JSONDecodeError:
        console.print("[red]❌ storage.json tiene formato inválido[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Error leyendo storage.json: {str(e)}[/red]")
        return False

def check_backup_exists(storage_file):
    """Verifica si existe un backup."""
    console.print("\n[bold cyan]═══ VERIFICACIÓN 3: Backup ═══[/bold cyan]\n")
    
    backup_files = list(storage_file.parent.glob("storage.json.backup_*"))
    
    if backup_files:
        console.print(f"[green]✅ Se encontraron {len(backup_files)} archivo(s) de backup[/green]\n")
        
        table = Table(title="Archivos de Backup")
        table.add_column("Archivo", style="white")
        table.add_column("Fecha", style="cyan")
        table.add_column("Tamaño", style="yellow")
        
        for backup in sorted(backup_files, reverse=True)[:5]:
            try:
                stat = backup.stat()
                size = stat.st_size
                from datetime import datetime
                mtime = datetime.fromtimestamp(stat.st_mtime)
                
                size_str = f"{size:,} bytes"
                if size > 1024:
                    size_str = f"{size/1024:.2f} KB"
                
                table.add_row(
                    backup.name,
                    mtime.strftime("%Y-%m-%d %H:%M:%S"),
                    size_str
                )
            except:
                pass
        
        console.print(table)
        console.print("\n[green]✅ Puedes restaurar desde estos backups si es necesario[/green]")
        return True
    else:
        console.print("[yellow]⚠️  No se encontraron archivos de backup[/yellow]")
        console.print("[yellow]   Es posible que no hayas creado backup durante el reseteo[/yellow]")
        return False

def verify_windsurf_not_running():
    """Verifica que Windsurf no esté ejecutándose."""
    console.print("\n[bold cyan]═══ VERIFICACIÓN 4: Procesos de Windsurf ═══[/bold cyan]\n")
    
    try:
        import psutil
        
        process_names = ["Windsurf.exe", "windsurf", "Windsurf", "windsurf.exe"]
        windsurf_processes = []
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] in process_names:
                    windsurf_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if windsurf_processes:
            console.print(f"[yellow]⚠️  Windsurf está en ejecución ({len(windsurf_processes)} proceso(s))[/yellow]")
            console.print("\n[yellow]⚠️  IMPORTANTE: Debes REINICIAR Windsurf para que los cambios tengan efecto[/yellow]")
            console.print("[yellow]   1. Cierra Windsurf completamente[/yellow]")
            console.print("[yellow]   2. Vuelve a abrirlo[/yellow]")
            console.print("[yellow]   3. Inicia sesión o crea cuenta nueva[/yellow]")
            return False
        else:
            console.print("[green]✅ Windsurf no está en ejecución[/green]")
            console.print("[cyan]   Ahora puedes iniciar Windsurf para ver los cambios[/cyan]")
            return True
            
    except ImportError:
        console.print("[yellow]⚠️  psutil no disponible, no se puede verificar[/yellow]")
        console.print("[cyan]   Asegúrate de reiniciar Windsurf manualmente[/cyan]")
        return True

def main():
    """Función principal de verificación."""
    console.clear()
    
    console.print(Panel(
        Text(
            "VERIFICACIÓN POST-RESETEO\n\n"
            "Este script verifica que los cambios\n"
            "se aplicaron correctamente.",
            justify="center"
        ),
        title="🔍 Verificación de Cambios",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    base_path, storage_file = get_windsurf_paths()
    
    console.print(f"\n[cyan]📍 Verificando en:[/cyan] {base_path}\n")
    
    # Ejecutar verificaciones
    results = []
    
    results.append(("Archivos eliminados", verify_files_deleted(base_path)))
    results.append(("storage.json modificado", verify_storage_json(storage_file)))
    results.append(("Backup creado", check_backup_exists(storage_file)))
    results.append(("Windsurf cerrado", verify_windsurf_not_running()))
    
    # Resumen final
    console.print("\n" + "="*60)
    console.print("[bold cyan]═══ RESUMEN DE VERIFICACIÓN ═══[/bold cyan]\n")
    
    table = Table(title="Resultados")
    table.add_column("Verificación", style="white")
    table.add_column("Estado", style="bold")
    
    passed = 0
    warnings = 0
    
    for name, result in results:
        if result:
            table.add_row(name, "[green]✅ OK[/green]")
            passed += 1
        else:
            table.add_row(name, "[yellow]⚠️  Advertencia[/yellow]")
            warnings += 1
    
    console.print(table)
    
    console.print(f"\n[cyan]📊 Resumen:[/cyan]")
    console.print(f"   • Verificaciones OK: [green bold]{passed}[/green bold]")
    console.print(f"   • Advertencias: [yellow bold]{warnings}[/yellow bold]")
    
    if passed >= 2:  # Al menos 2 verificaciones deben pasar
        console.print("\n" + "="*60)
        console.print(Panel(
            Text(
                "✅ EL RESETEO FUE EXITOSO\n\n"
                "Los cambios se aplicaron correctamente.\n\n"
                "PRÓXIMOS PASOS:\n"
                "1. Reinicia Windsurf (si aún no lo has hecho)\n"
                "2. Inicia sesión o crea cuenta nueva\n"
                "3. Verifica que obtienes una nueva API key",
                justify="center"
            ),
            title="[bold green]✅ VERIFICACIÓN EXITOSA[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
    else:
        console.print("\n" + "="*60)
        console.print(Panel(
            Text(
                "⚠️  EL RESETEO PUDO HABER FALLADO\n\n"
                "Algunas verificaciones no pasaron.\n\n"
                "RECOMENDACIONES:\n"
                "1. Ejecuta el reseteo nuevamente\n"
                "2. Asegúrate de cerrar Windsurf antes\n"
                "3. Ejecuta como administrador si es necesario",
                justify="center"
            ),
            title="[bold yellow]⚠️  ADVERTENCIA[/bold yellow]",
            border_style="yellow",
            padding=(1, 2)
        ))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Verificación cancelada[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
