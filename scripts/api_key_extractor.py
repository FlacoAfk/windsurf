"""
Script para extraer y verificar la API key de Windsurf de forma segura.
Este script lee la API key sin exponerla completamente en la terminal.
"""
import json
import platform
from pathlib import Path
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


def mask_api_key(api_key: str, visible_chars: int = 8) -> str:
    """
    Enmascara la API key mostrando solo los primeros y últimos caracteres.
    
    Args:
        api_key: La API key completa
        visible_chars: Número de caracteres visibles al inicio y al final
    
    Returns:
        API key enmascarada
    """
    if not api_key or len(api_key) < visible_chars * 2:
        return "***INVALID***"
    
    start = api_key[:visible_chars]
    end = api_key[-visible_chars:]
    middle_length = len(api_key) - (visible_chars * 2)
    
    return f"{start}{'*' * middle_length}{end}"


def find_api_keys_in_storage(storage_file: Path) -> dict:
    """
    Busca posibles API keys en el archivo storage.json.
    
    Returns:
        Diccionario con las claves encontradas y sus valores enmascarados
    """
    if not storage_file.exists():
        return {}
    
    try:
        with open(storage_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Buscar claves que puedan contener API keys
        api_key_patterns = ['api', 'key', 'token', 'auth', 'secret', 'codeium', 'windsurf']
        potential_keys = {}
        
        for key, value in data.items():
            key_lower = key.lower()
            if any(pattern in key_lower for pattern in api_key_patterns):
                if isinstance(value, str) and len(value) > 20:  # Probablemente sea una key
                    potential_keys[key] = {
                        'value': value,
                        'masked': mask_api_key(value),
                        'length': len(value)
                    }
        
        return potential_keys
    
    except Exception as e:
        console.print(f"[red]Error leyendo storage.json: {str(e)}[/red]")
        return {}


def check_local_storage(base_path: Path) -> dict:
    """
    Verifica si existen archivos de Local Storage que puedan contener API keys.
    
    Returns:
        Información sobre los archivos encontrados
    """
    local_storage_path = base_path / "Local Storage" / "leveldb"
    
    if not local_storage_path.exists():
        return {'exists': False}
    
    try:
        files = list(local_storage_path.glob('*'))
        return {
            'exists': True,
            'file_count': len(files),
            'files': [f.name for f in files[:5]]  # Solo los primeros 5
        }
    except Exception as e:
        return {'exists': True, 'error': str(e)}


def main():
    """Función principal."""
    console.print(Panel(
        Text("API Key Extractor - Windsurf Reset Tool", justify="center"),
        title="🔑 API Key Security Check",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    try:
        # Obtener rutas
        base_path = get_windsurf_base_path()
        storage_file = base_path / "User" / "globalStorage" / "storage.json"
        
        console.print(f"[cyan]📁 Ruta de Windsurf: {base_path}[/cyan]\n")
        
        # Verificar storage.json
        console.print("[bold]1. Verificando storage.json[/bold]")
        if storage_file.exists():
            console.print(f"[green]   ✅ Archivo encontrado: {storage_file}[/green]")
            
            # Buscar API keys
            api_keys = find_api_keys_in_storage(storage_file)
            
            if api_keys:
                console.print(f"\n[yellow]⚠️  Se encontraron {len(api_keys)} posible(s) API key(s):[/yellow]\n")
                
                table = Table(title="Claves Encontradas (Enmascaradas)")
                table.add_column("Clave", style="cyan")
                table.add_column("Valor Enmascarado", style="yellow")
                table.add_column("Longitud", style="green")
                
                for key_name, key_info in api_keys.items():
                    table.add_row(
                        key_name,
                        key_info['masked'],
                        str(key_info['length'])
                    )
                
                console.print(table)
                
                console.print("\n[bold red]⚠️  IMPORTANTE - SEGURIDAD:[/bold red]")
                console.print("[red]• NUNCA compartas estas claves completas[/red]")
                console.print("[red]• Si las compartiste por accidente, ejecuta el reset inmediatamente[/red]")
                console.print("[red]• Después del reset, verifica que sean diferentes[/red]")
            else:
                console.print("[green]   ✅ No se encontraron API keys evidentes[/green]")
        else:
            console.print("[yellow]   ⚠️  storage.json no existe[/yellow]")
        
        # Verificar Local Storage
        console.print("\n[bold]2. Verificando Local Storage[/bold]")
        local_storage_info = check_local_storage(base_path)
        
        if local_storage_info['exists']:
            console.print("[green]   ✅ Local Storage existe[/green]")
            if 'file_count' in local_storage_info:
                console.print(f"[cyan]   📊 Archivos encontrados: {local_storage_info['file_count']}[/cyan]")
                console.print("[yellow]   ⚠️  API keys pueden estar almacenadas aquí[/yellow]")
        else:
            console.print("[yellow]   ⚠️  Local Storage no existe[/yellow]")
        
        # Recomendaciones
        console.print("\n" + "="*60)
        console.print(Panel(
            Text(
                "Recomendaciones de Seguridad:\n\n"
                "1. Si compartiste una API key, ejecuta el reset inmediatamente\n"
                "2. Después del reset, verifica que la API key sea diferente\n"
                "3. Nunca compartas claves completas, solo versiones enmascaradas\n"
                "4. Usa variables de entorno para almacenar keys en desarrollo",
                justify="left"
            ),
            title="🛡️  Seguridad",
            border_style="green",
            padding=(1, 2)
        ))
        
    except Exception as e:
        console.print(Panel(
            Text(f"Error: {str(e)}", justify="center"),
            title="❌ Error",
            border_style="red",
            padding=(1, 2)
        ))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operación cancelada por el usuario[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error fatal: {str(e)}[/red]")
