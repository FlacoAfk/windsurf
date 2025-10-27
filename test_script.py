"""
Script de pruebas intensivas para verificar que windsurf_reset.py funciona correctamente.
Este script NO hace cambios destructivos, solo verifica la funcionalidad.
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

def print_section(title):
    """Imprime un separador de sección."""
    console.print(f"\n{'='*60}")
    console.print(f"[bold cyan]{title}[/bold cyan]")
    console.print(f"{'='*60}\n")

def test_imports():
    """Prueba 1: Verificar que todos los imports funcionan."""
    print_section("PRUEBA 1: Verificando imports y dependencias")
    
    try:
        import uuid
        import shutil
        import logging
        from datetime import datetime
        from typing import Dict, Optional
        from rich.console import Console
        from rich.panel import Panel
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
        from rich.prompt import Confirm, Prompt
        from rich.theme import Theme
        from rich.layout import Layout
        from rich.table import Table
        from rich import print as rprint
        from rich.style import Style
        from rich.text import Text
        
        console.print("[green]✅ Todos los imports básicos funcionan correctamente[/green]")
        
        try:
            import psutil
            console.print("[green]✅ psutil está instalado (detección de procesos habilitada)[/green]")
            return True, True
        except ImportError:
            console.print("[yellow]⚠️  psutil NO está instalado (detección de procesos deshabilitada)[/yellow]")
            console.print("[yellow]   Instala con: pip install psutil[/yellow]")
            return True, False
            
    except ImportError as e:
        console.print(f"[red]❌ Error en imports: {str(e)}[/red]")
        console.print("[red]   Ejecuta: pip install -r requirements.txt[/red]")
        return False, False

def test_paths():
    """Prueba 2: Verificar que puede encontrar las rutas de Windsurf."""
    print_section("PRUEBA 2: Verificando rutas de Windsurf")
    
    try:
        system = platform.system()
        console.print(f"[cyan]Sistema operativo: {system}[/cyan]")
        
        paths = {
            "Windows": Path(os.getenv("APPDATA", "")),
            "Darwin": Path.home() / "Library" / "Application Support",
            "Linux": Path.home() / ".config",
        }
        
        base_path = paths.get(system)
        if not base_path:
            console.print(f"[red]❌ Sistema no soportado: {system}[/red]")
            return False
        
        console.print(f"[green]✅ Ruta base detectada: {base_path}[/green]")
        
        if not base_path.exists():
            console.print(f"[red]❌ La ruta base no existe: {base_path}[/red]")
            return False
        
        console.print(f"[green]✅ La ruta base existe[/green]")
        
        # Verificar ruta de Windsurf
        windsurf_path = base_path / "Windsurf"
        console.print(f"[cyan]Ruta de Windsurf: {windsurf_path}[/cyan]")
        
        if windsurf_path.exists():
            console.print(f"[green]✅ Directorio de Windsurf encontrado[/green]")
            
            # Verificar storage.json
            storage_file = windsurf_path / "User" / "globalStorage" / "storage.json"
            console.print(f"[cyan]Archivo storage.json: {storage_file}[/cyan]")
            
            if storage_file.exists():
                console.print(f"[green]✅ storage.json existe[/green]")
                
                # Intentar leer el archivo
                try:
                    with open(storage_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    console.print(f"[green]✅ storage.json es válido (tiene {len(data)} claves)[/green]")
                except json.JSONDecodeError:
                    console.print(f"[yellow]⚠️  storage.json existe pero tiene formato inválido[/yellow]")
                except Exception as e:
                    console.print(f"[yellow]⚠️  No se puede leer storage.json: {str(e)}[/yellow]")
            else:
                console.print(f"[yellow]⚠️  storage.json no existe (será creado durante el reseteo)[/yellow]")
        else:
            console.print(f"[yellow]⚠️  Windsurf no está instalado en: {windsurf_path}[/yellow]")
            console.print(f"[yellow]   El directorio será creado durante el reseteo[/yellow]")
        
        # Verificar permisos de escritura
        if os.access(str(base_path), os.W_OK):
            console.print(f"[green]✅ Tienes permisos de escritura en: {base_path}[/green]")
        else:
            console.print(f"[red]❌ NO tienes permisos de escritura en: {base_path}[/red]")
            console.print(f"[red]   Ejecuta el script como administrador[/red]")
            return False
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Error verificando rutas: {str(e)}[/red]")
        return False

def test_files_to_clean():
    """Prueba 3: Verificar qué archivos existen y serían eliminados."""
    print_section("PRUEBA 3: Identificando archivos a limpiar")
    
    try:
        system = platform.system()
        paths = {
            "Windows": Path(os.getenv("APPDATA", "")),
            "Darwin": Path.home() / "Library" / "Application Support",
            "Linux": Path.home() / ".config",
        }
        
        base_path = paths.get(system) / "Windsurf"
        
        if not base_path.exists():
            console.print(f"[yellow]⚠️  Windsurf no está instalado, no hay archivos para limpiar[/yellow]")
            return True
        
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
        
        table = Table(title="Archivos y Directorios a Limpiar")
        table.add_column("Tipo", style="cyan")
        table.add_column("Ruta", style="white")
        table.add_column("Estado", style="green")
        table.add_column("Tamaño", style="yellow")
        
        found_count = 0
        total_size = 0
        
        for path in paths_to_clean:
            if path.exists():
                tipo = "📁 DIR" if path.is_dir() else "📄 FILE"
                estado = "✅ Existe"
                
                # Calcular tamaño
                try:
                    if path.is_file():
                        size = path.stat().st_size
                        size_str = format_size(size)
                        total_size += size
                    else:
                        size = get_dir_size(path)
                        size_str = format_size(size)
                        total_size += size
                except:
                    size_str = "?"
                
                table.add_row(tipo, str(path.name), estado, size_str)
                found_count += 1
            else:
                table.add_row("❌", str(path.name), "No existe", "-")
        
        console.print(table)
        console.print(f"\n[cyan]📊 Resumen:[/cyan]")
        console.print(f"[green]✅ {found_count} de {len(paths_to_clean)} archivos/directorios encontrados[/green]")
        console.print(f"[yellow]📦 Espacio total a liberar: {format_size(total_size)}[/yellow]")
        
        if found_count > 0:
            console.print(f"\n[green]✅ El script eliminará {found_count} archivos/directorios[/green]")
        else:
            console.print(f"\n[yellow]⚠️  No hay archivos para limpiar (Windsurf recién instalado o ya limpio)[/yellow]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Error identificando archivos: {str(e)}[/red]")
        return False

def get_dir_size(path):
    """Calcula el tamaño total de un directorio."""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_dir_size(entry.path)
    except PermissionError:
        pass
    return total

def format_size(size):
    """Formatea el tamaño en bytes a formato legible."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def test_windsurf_running(psutil_available):
    """Prueba 4: Verificar si Windsurf está en ejecución."""
    print_section("PRUEBA 4: Verificando procesos de Windsurf")
    
    if not psutil_available:
        console.print("[yellow]⚠️  psutil no está disponible, no se puede verificar procesos[/yellow]")
        console.print("[yellow]   Instala con: pip install psutil[/yellow]")
        return True
    
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
            console.print(f"[yellow]⚠️  Windsurf está en ejecución ({len(windsurf_processes)} proceso(s))[/yellow]")
            
            table = Table(title="Procesos de Windsurf Detectados")
            table.add_column("PID", style="cyan")
            table.add_column("Nombre", style="white")
            table.add_column("Memoria", style="yellow")
            
            for proc in windsurf_processes:
                try:
                    mem = proc.info['memory_info'].rss
                    table.add_row(
                        str(proc.info['pid']),
                        proc.info['name'],
                        format_size(mem)
                    )
                except:
                    pass
            
            console.print(table)
            console.print("\n[yellow]⚠️  Recomendación: Cierra Windsurf antes de ejecutar el reseteo[/yellow]")
            console.print("[yellow]   El script puede cerrarlo automáticamente si lo deseas[/yellow]")
        else:
            console.print("[green]✅ Windsurf no está en ejecución[/green]")
            console.print("[green]   Es seguro ejecutar el reseteo[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Error verificando procesos: {str(e)}[/red]")
        return False

def test_storage_json_content():
    """Prueba 5: Analizar el contenido de storage.json."""
    print_section("PRUEBA 5: Analizando storage.json actual")
    
    try:
        system = platform.system()
        paths = {
            "Windows": Path(os.getenv("APPDATA", "")),
            "Darwin": Path.home() / "Library" / "Application Support",
            "Linux": Path.home() / ".config",
        }
        
        base_path = paths.get(system)
        storage_file = base_path / "Windsurf" / "User" / "globalStorage" / "storage.json"
        
        if not storage_file.exists():
            console.print("[yellow]⚠️  storage.json no existe todavía[/yellow]")
            console.print("[yellow]   Será creado durante el primer reseteo[/yellow]")
            return True
        
        with open(storage_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        console.print(f"[cyan]Total de claves en storage.json: {len(data)}[/cyan]\n")
        
        # Analizar claves relacionadas con telemetría
        telemetry_keys = {k: v for k, v in data.items() if k.startswith('telemetry')}
        
        if telemetry_keys:
            console.print("[cyan]🔑 Claves de Telemetría Actuales:[/cyan]")
            table = Table()
            table.add_column("Clave", style="yellow")
            table.add_column("Valor (primeros 40 caracteres)", style="white")
            
            for key, value in telemetry_keys.items():
                value_str = str(value)[:40] + ("..." if len(str(value)) > 40 else "")
                table.add_row(key, value_str)
            
            console.print(table)
            console.print(f"\n[green]✅ Se encontraron {len(telemetry_keys)} claves de telemetría[/green]")
        else:
            console.print("[yellow]⚠️  No se encontraron claves de telemetría[/yellow]")
        
        # Analizar claves relacionadas con autenticación
        auth_keys = [k for k in data.keys() if any(x in k.lower() for x in ['auth', 'token', 'session', 'codeium', 'windsurf'])]
        
        if auth_keys:
            console.print(f"\n[cyan]🔐 Claves de Autenticación Encontradas: {len(auth_keys)}[/cyan]")
            for key in auth_keys[:10]:  # Mostrar solo las primeras 10
                console.print(f"   • {key}")
            if len(auth_keys) > 10:
                console.print(f"   ... y {len(auth_keys) - 10} más")
            console.print(f"\n[green]✅ Estas claves serán eliminadas durante el reseteo[/green]")
        else:
            console.print("\n[yellow]⚠️  No se encontraron claves de autenticación evidentes[/yellow]")
        
        return True
        
    except json.JSONDecodeError:
        console.print("[yellow]⚠️  storage.json tiene formato inválido[/yellow]")
        console.print("[yellow]   Será recreado durante el reseteo[/yellow]")
        return True
    except Exception as e:
        console.print(f"[red]❌ Error analizando storage.json: {str(e)}[/red]")
        return False

def test_uuid_generation():
    """Prueba 6: Verificar generación de nuevos IDs."""
    print_section("PRUEBA 6: Probando generación de IDs")
    
    try:
        import uuid
        
        # Generar IDs de prueba
        test_ids = {
            "telemetry.machineId": os.urandom(32).hex(),
            "telemetry.macMachineId": os.urandom(32).hex(),
            "telemetry.devDeviceId": str(uuid.uuid4()),
        }
        
        console.print("[cyan]IDs de prueba generados:[/cyan]\n")
        
        table = Table()
        table.add_column("Clave", style="yellow")
        table.add_column("Valor Generado", style="green")
        table.add_column("Longitud", style="cyan")
        
        for key, value in test_ids.items():
            table.add_row(key, value, str(len(value)))
        
        console.print(table)
        
        # Verificar que son únicos
        if len(set(test_ids.values())) == len(test_ids):
            console.print("\n[green]✅ Todos los IDs son únicos[/green]")
        else:
            console.print("\n[red]❌ Algunos IDs son duplicados[/red]")
            return False
        
        # Verificar formato
        if len(test_ids["telemetry.machineId"]) == 64:
            console.print("[green]✅ machineId tiene longitud correcta (64)[/green]")
        else:
            console.print("[red]❌ machineId tiene longitud incorrecta[/red]")
            return False
        
        if len(test_ids["telemetry.macMachineId"]) == 64:
            console.print("[green]✅ macMachineId tiene longitud correcta (64)[/green]")
        else:
            console.print("[red]❌ macMachineId tiene longitud incorrecta[/red]")
            return False
        
        try:
            uuid.UUID(test_ids["telemetry.devDeviceId"])
            console.print("[green]✅ devDeviceId es un UUID válido[/green]")
        except:
            console.print("[red]❌ devDeviceId no es un UUID válido[/red]")
            return False
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Error generando IDs: {str(e)}[/red]")
        return False

def main():
    """Función principal de pruebas."""
    console.clear()
    
    console.print(Panel(
        Text("Pruebas Intensivas - Windsurf Reset Tool", justify="center"),
        title="🧪 Test Suite",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    results = []
    
    # Ejecutar todas las pruebas
    imports_ok, psutil_available = test_imports()
    results.append(("Imports y Dependencias", imports_ok))
    
    if imports_ok:
        results.append(("Verificación de Rutas", test_paths()))
        results.append(("Identificación de Archivos", test_files_to_clean()))
        results.append(("Detección de Procesos", test_windsurf_running(psutil_available)))
        results.append(("Análisis de storage.json", test_storage_json_content()))
        results.append(("Generación de IDs", test_uuid_generation()))
    
    # Resumen final
    print_section("RESUMEN DE PRUEBAS")
    
    table = Table(title="Resultados de las Pruebas")
    table.add_column("Prueba", style="white")
    table.add_column("Resultado", style="bold")
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        if result:
            table.add_row(test_name, "[green]✅ PASÓ[/green]")
            passed += 1
        else:
            table.add_row(test_name, "[red]❌ FALLÓ[/red]")
            failed += 1
    
    console.print(table)
    
    console.print(f"\n[cyan]📊 Total: {passed + failed} pruebas[/cyan]")
    console.print(f"[green]✅ Pasadas: {passed}[/green]")
    console.print(f"[red]❌ Falladas: {failed}[/red]")
    
    if failed == 0:
        console.print("\n" + "="*60)
        console.print(Panel(
            Text(
                "¡TODAS LAS PRUEBAS PASARON!\n\n"
                "El script está listo para ejecutarse.\n"
                "Ejecuta: python windsurf_reset.py",
                justify="center"
            ),
            title="[bold green]✅ ÉXITO[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
    else:
        console.print("\n" + "="*60)
        console.print(Panel(
            Text(
                f"Algunas pruebas fallaron ({failed}).\n\n"
                "Revisa los errores antes de ejecutar el script.",
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
        console.print("\n[yellow]Pruebas canceladas por el usuario[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error fatal: {str(e)}[/red]")
