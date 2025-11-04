"""
Script de verificación post-reset para Windsurf Reset Tool.
Compara el estado antes y después del reset para confirmar que los cambios se aplicaron.
"""
import json
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def get_windsurf_base_path() -> Path:
    """Obtiene la ruta base de Windsurf."""
    system = platform.system()
    paths = {
        "Windows": Path.home() / "AppData" / "Roaming",
        "Darwin": Path.home() / "Library" / "Application Support",
        "Linux": Path.home() / ".config",
    }
    
    base_path = paths.get(system)
    if not base_path:
        raise Exception(f"Sistema operativo no soportado: {system}")
    
    return base_path / "Windsurf"


def get_device_ids(storage_file: Path) -> Dict[str, str]:
    """
    Extrae los Device IDs del storage.json.
    
    Returns:
        Diccionario con los IDs de dispositivo
    """
    if not storage_file.exists():
        return {}
    
    try:
        with open(storage_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extraer IDs de telemetría
        return {k: v for k, v in data.items() if k.startswith('telemetry')}
    except Exception:
        return {}


def check_files_exist(base_path: Path) -> Dict[str, bool]:
    """
    Verifica qué archivos de sesión/cache existen.
    
    Returns:
        Diccionario con nombre de archivo y si existe
    """
    files_to_check = [
        ("Cookies", base_path / "Cookies"),
        ("Cookies-journal", base_path / "Cookies-journal"),
        ("Network Persistent State", base_path / "Network Persistent State"),
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
    
    return {name: path.exists() for name, path in files_to_check}


def compare_ids(before_ids: Dict[str, str], after_ids: Dict[str, str]) -> List[Tuple[str, bool, str, str]]:
    """
    Compara IDs antes y después.
    
    Returns:
        Lista de tuplas (nombre, cambió, valor_antes, valor_después)
    """
    all_keys = set(before_ids.keys()) | set(after_ids.keys())
    comparisons = []
    
    for key in sorted(all_keys):
        before_val = before_ids.get(key, "N/A")
        after_val = after_ids.get(key, "N/A")
        changed = before_val != after_val
        comparisons.append((key, changed, before_val, after_val))
    
    return comparisons


def save_state_snapshot(base_path: Path, prefix: str = "before"):
    """
    Guarda un snapshot del estado actual.
    
    Args:
        base_path: Ruta base de Windsurf
        prefix: Prefijo para el archivo (before/after)
    """
    storage_file = base_path / "User" / "globalStorage" / "storage.json"
    
    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'device_ids': get_device_ids(storage_file),
        'files_exist': check_files_exist(base_path)
    }
    
    snapshot_file = Path(__file__).parent / f"snapshot_{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(snapshot_file, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2)
    
    return snapshot_file


def mask_value(value: str, visible_chars: int = 8) -> str:
    """Enmascara un valor mostrando solo inicio y final."""
    if len(value) <= visible_chars * 2:
        return value
    return f"{value[:visible_chars]}...{value[-visible_chars:]}"


def verify_reset():
    """Verifica que el reset se haya aplicado correctamente."""
    console.print(Panel(
        Text("Post-Reset Verification Tool", justify="center"),
        title="🔍 Verificación de Reset",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    try:
        base_path = get_windsurf_base_path()
        storage_file = base_path / "User" / "globalStorage" / "storage.json"
        
        console.print(f"[cyan]📁 Verificando: {base_path}[/cyan]\n")
        
        # 1. Verificar Device IDs
        console.print("[bold]1. Verificando Device IDs[/bold]")
        current_ids = get_device_ids(storage_file)
        
        if current_ids:
            table = Table(title="Device IDs Actuales")
            table.add_column("Clave", style="cyan")
            table.add_column("Valor (enmascarado)", style="yellow")
            
            for key, value in current_ids.items():
                table.add_row(key, mask_value(str(value)))
            
            console.print(table)
            console.print(f"[green]   ✅ Se encontraron {len(current_ids)} Device IDs[/green]")
        else:
            console.print("[yellow]   ⚠️  No se encontraron Device IDs (storage.json vacío)[/yellow]")
        
        # 2. Verificar archivos eliminados
        console.print("\n[bold]2. Verificando archivos de sesión/cache[/bold]")
        files_status = check_files_exist(base_path)
        
        table = Table(title="Estado de Archivos")
        table.add_column("Archivo", style="white")
        table.add_column("Estado", style="cyan")
        
        existing_count = 0
        for name, exists in files_status.items():
            if exists:
                table.add_row(name, "[yellow]⚠️  Existe[/yellow]")
                existing_count += 1
            else:
                table.add_row(name, "[green]✅ Eliminado[/green]")
        
        console.print(table)
        
        if existing_count == 0:
            console.print("\n[bold green]✅ PERFECTO: Todos los archivos fueron eliminados[/bold green]")
        else:
            console.print(f"\n[yellow]⚠️  ADVERTENCIA: {existing_count} archivo(s) todavía existe(n)[/yellow]")
            console.print("[yellow]   Esto es normal si Windsurf está actualmente abierto[/yellow]")
        
        # 3. Verificar storage.json
        console.print("\n[bold]3. Verificando storage.json[/bold]")
        if storage_file.exists():
            try:
                with open(storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Buscar claves sospechosas
                suspicious_keys = [k for k in data.keys() if any(
                    x in k.lower() for x in ['auth', 'token', 'session', 'codeium.token']
                )]
                
                console.print(f"[cyan]   Total de claves: {len(data)}[/cyan]")
                
                if suspicious_keys:
                    console.print(f"[yellow]   ⚠️  {len(suspicious_keys)} clave(s) de autenticación encontrada(s):[/yellow]")
                    for key in suspicious_keys[:5]:
                        console.print(f"      • {key}")
                    if len(suspicious_keys) > 5:
                        console.print(f"      ... y {len(suspicious_keys) - 5} más")
                else:
                    console.print("[green]   ✅ No se encontraron claves de autenticación antiguas[/green]")
                
            except json.JSONDecodeError:
                console.print("[red]   ❌ storage.json tiene formato inválido[/red]")
        else:
            console.print("[yellow]   ⚠️  storage.json no existe[/yellow]")
        
        # 4. Recomendaciones
        console.print("\n" + "="*60)
        console.print(Panel(
            Text(
                "Próximos Pasos:\n\n"
                "1. REINICIA Windsurf completamente\n"
                "2. Inicia sesión con tu cuenta\n"
                "3. Verifica que la API key sea diferente\n"
                "4. Si la API key es la misma, ejecuta el reset nuevamente\n\n"
                "Nota: Los cambios NO se aplican hasta reiniciar Windsurf",
                justify="left"
            ),
            title="📝 Recomendaciones",
            border_style="green",
            padding=(1, 2)
        ))
        
        # Opción para guardar snapshot
        console.print("\n[cyan]¿Deseas guardar un snapshot del estado actual? (s/n)[/cyan]")
        # Para automatización, solo mostramos la opción
        console.print("[dim]Ejecuta con --snapshot para guardar automáticamente[/dim]")
        
    except Exception as e:
        console.print(Panel(
            Text(f"Error: {str(e)}", justify="center"),
            title="❌ Error",
            border_style="red",
            padding=(1, 2)
        ))


def compare_snapshots(before_file: Path, after_file: Path):
    """
    Compara dos snapshots para ver las diferencias.
    
    Args:
        before_file: Archivo snapshot "antes"
        after_file: Archivo snapshot "después"
    """
    console.print(Panel(
        Text("Snapshot Comparison Tool", justify="center"),
        title="🔄 Comparación de Snapshots",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    try:
        # Cargar snapshots
        with open(before_file, 'r', encoding='utf-8') as f:
            before = json.load(f)
        
        with open(after_file, 'r', encoding='utf-8') as f:
            after = json.load(f)
        
        # Comparar IDs
        console.print("[bold]Comparación de Device IDs:[/bold]\n")
        
        comparisons = compare_ids(before['device_ids'], after['device_ids'])
        
        table = Table(title="Cambios en Device IDs")
        table.add_column("Clave", style="cyan")
        table.add_column("Estado", style="yellow")
        table.add_column("Antes", style="red")
        table.add_column("Después", style="green")
        
        changed_count = 0
        for key, changed, before_val, after_val in comparisons:
            if changed:
                changed_count += 1
                status = "✅ CAMBIÓ"
            else:
                status = "❌ SIN CAMBIO"
            
            table.add_row(
                key,
                status,
                mask_value(str(before_val)),
                mask_value(str(after_val))
            )
        
        console.print(table)
        
        if changed_count > 0:
            console.print(f"\n[bold green]✅ {changed_count} ID(s) cambiaron correctamente[/bold green]")
        else:
            console.print("\n[bold red]❌ Ningún ID cambió - El reset puede no haber funcionado[/bold red]")
        
        # Comparar archivos
        console.print("\n[bold]Comparación de Archivos:[/bold]\n")
        
        before_files = before['files_exist']
        after_files = after['files_exist']
        
        table = Table(title="Estado de Archivos")
        table.add_column("Archivo", style="white")
        table.add_column("Antes", style="red")
        table.add_column("Después", style="green")
        table.add_column("Estado", style="cyan")
        
        deleted_count = 0
        for file_name in before_files.keys():
            before_exists = before_files[file_name]
            after_exists = after_files.get(file_name, False)
            
            if before_exists and not after_exists:
                status = "✅ ELIMINADO"
                deleted_count += 1
            elif before_exists and after_exists:
                status = "❌ SIGUE EXISTIENDO"
            elif not before_exists and not after_exists:
                status = "ℹ️  NO EXISTÍA"
            else:
                status = "⚠️  CREADO"
            
            table.add_row(
                file_name,
                "✓" if before_exists else "✗",
                "✓" if after_exists else "✗",
                status
            )
        
        console.print(table)
        
        if deleted_count > 0:
            console.print(f"\n[bold green]✅ {deleted_count} archivo(s) fueron eliminados[/bold green]")
        else:
            console.print("\n[bold yellow]⚠️  No se eliminaron archivos[/bold yellow]")
        
    except Exception as e:
        console.print(Panel(
            Text(f"Error: {str(e)}", justify="center"),
            title="❌ Error",
            border_style="red",
            padding=(1, 2)
        ))


if __name__ == "__main__":
    import sys
    
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "--snapshot":
                # Guardar snapshot
                base_path = get_windsurf_base_path()
                prefix = sys.argv[2] if len(sys.argv) > 2 else "manual"
                snapshot_file = save_state_snapshot(base_path, prefix)
                console.print(f"[green]✅ Snapshot guardado: {snapshot_file}[/green]")
            
            elif sys.argv[1] == "--compare":
                # Comparar snapshots
                if len(sys.argv) < 4:
                    console.print("[red]Uso: python post_reset_verify.py --compare <antes.json> <despues.json>[/red]")
                else:
                    compare_snapshots(Path(sys.argv[2]), Path(sys.argv[3]))
        else:
            # Verificación normal
            verify_reset()
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Operación cancelada[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
