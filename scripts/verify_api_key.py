"""
Script para verificar si la API key de Windsurf fue reseteada correctamente.
Compara la API key actual con la key antigua comprometida.
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

# API key antigua que fue comprometida (PLACEHOLDER - usar tu propia key comprometida)
OLD_COMPROMISED_KEY = "sk-ws-01-EXAMPLE-KEY-REPLACE-WITH-YOUR-COMPROMISED-KEY-IF-NEEDED"

def get_windsurf_base_path() -> Path:
    """Obtiene el directorio base de Windsurf."""
    system = platform.system()
    paths = {
        "Windows": Path(os.getenv("APPDATA", "")),
        "Darwin": Path.home() / "Library" / "Application Support",
        "Linux": Path.home() / ".config",
    }
    
    base_path = paths.get(system)
    if not base_path:
        raise Exception(f"Sistema operativo no soportado: {system}")
    
    return base_path / "Windsurf"

def get_storage_file() -> Path:
    """Obtiene la ruta del archivo storage.json."""
    return get_windsurf_base_path() / "User" / "globalStorage" / "storage.json"

def find_api_keys_in_storage(data: dict) -> list:
    """Busca posibles API keys en el storage."""
    api_keys = []
    
    # Buscar en todas las claves que puedan contener API keys
    for key, value in data.items():
        if isinstance(value, str):
            # Buscar patrones que se parezcan a API keys
            if value.startswith("sk-ws-") or "api" in key.lower() or "key" in key.lower():
                api_keys.append({
                    "key_name": key,
                    "value": value,
                    "is_compromised": value == OLD_COMPROMISED_KEY
                })
    
    return api_keys

def check_api_key_status():
    """Verifica el estado de la API key."""
    console.print("\n")
    console.print(Panel(
        "[bold cyan]Verificador de API Key - Windsurf[/bold cyan]\n"
        "Comprobando si tu API key fue reseteada correctamente...",
        title="🔍 Verificación de Seguridad",
        border_style="cyan"
    ))
    
    try:
        storage_file = get_storage_file()
        
        if not storage_file.exists():
            console.print(Panel(
                "[yellow]El archivo storage.json no existe.[/yellow]\n"
                "Esto significa que:\n"
                "• Windsurf no ha sido configurado aún, O\n"
                "• Los datos fueron completamente eliminados\n\n"
                "[green]✅ No hay riesgo de API key comprometida[/green]",
                title="ℹ️ Información",
                border_style="yellow"
            ))
            return
        
        # Leer el archivo
        with open(storage_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Buscar API keys
        api_keys = find_api_keys_in_storage(data)
        
        # Verificar IDs de telemetría
        telemetry_ids = {k: v for k, v in data.items() if k.startswith("telemetry")}
        
        # Mostrar resultados
        console.print("\n")
        
        # Tabla de IDs de telemetría
        if telemetry_ids:
            table = Table(title="📊 Identificadores de Dispositivo", border_style="blue")
            table.add_column("Clave", style="cyan")
            table.add_column("Valor", style="white")
            
            for key, value in telemetry_ids.items():
                table.add_row(key, str(value)[:40] + "..." if len(str(value)) > 40 else str(value))
            
            console.print(table)
        
        # Verificar API keys
        console.print("\n")
        if api_keys:
            console.print(Panel(
                "[bold yellow]⚠️ Se encontraron posibles API keys[/bold yellow]",
                border_style="yellow"
            ))
            
            for key_info in api_keys:
                key_value = key_info["value"]
                key_name = key_info["key_name"]
                is_compromised = key_info["is_compromised"]
                
                if is_compromised:
                    console.print(Panel(
                        f"[bold red]🚨 API KEY COMPROMETIDA DETECTADA[/bold red]\n\n"
                        f"Clave: {key_name}\n"
                        f"Valor: {key_value[:30]}...\n\n"
                        f"[bold]ACCIÓN REQUERIDA:[/bold]\n"
                        f"1. Ejecuta el script de reseteo: run_reset.bat\n"
                        f"2. Reinicia tu computadora\n"
                        f"3. Abre Windsurf para generar nueva API key",
                        title="❌ ALERTA DE SEGURIDAD",
                        border_style="red"
                    ))
                else:
                    # Mostrar solo primeros y últimos caracteres por seguridad
                    masked_value = key_value[:10] + "..." + key_value[-10:] if len(key_value) > 20 else "***"
                    console.print(Panel(
                        f"[bold green]✅ API Key encontrada (parece nueva)[/bold green]\n\n"
                        f"Clave: {key_name}\n"
                        f"Valor: {masked_value}\n\n"
                        f"[bold]No es la key comprometida[/bold]\n"
                        f"Recuerda: [yellow]NUNCA compartas esta key públicamente[/yellow]",
                        title="✓ API Key Verificada",
                        border_style="green"
                    ))
        else:
            console.print(Panel(
                "[bold green]✅ No se encontraron API keys en storage.json[/bold green]\n\n"
                "Esto es normal si:\n"
                "• Acabas de resetear Windsurf\n"
                "• Windsurf aún no ha generado una nueva key\n\n"
                "[cyan]Próximos pasos:[/cyan]\n"
                "1. Abre Windsurf\n"
                "2. Inicia sesión si es necesario\n"
                "3. Windsurf generará automáticamente una nueva API key",
                title="ℹ️ Estado",
                border_style="green"
            ))
        
        # Resumen final
        console.print("\n")
        summary_text = Text()
        summary_text.append("📝 Resumen de Verificación\n\n", style="bold cyan")
        summary_text.append(f"• Archivo storage.json: ", style="white")
        summary_text.append("✓ Encontrado\n", style="green")
        summary_text.append(f"• IDs de telemetría: ", style="white")
        summary_text.append(f"✓ {len(telemetry_ids)} encontrados\n", style="green")
        summary_text.append(f"• Posibles API keys: ", style="white")
        summary_text.append(f"{len(api_keys)} encontradas\n", style="cyan")
        
        # Verificar si la key comprometida está presente
        has_compromised = any(k["is_compromised"] for k in api_keys)
        summary_text.append(f"• Key comprometida: ", style="white")
        if has_compromised:
            summary_text.append("❌ PRESENTE - ACCIÓN REQUERIDA\n", style="bold red")
        else:
            summary_text.append("✓ No detectada\n", style="green")
        
        console.print(Panel(summary_text, border_style="cyan"))
        
    except json.JSONDecodeError:
        console.print(Panel(
            "[red]Error: El archivo storage.json tiene formato inválido[/red]\n\n"
            "Esto puede indicar que el archivo está corrupto.\n"
            "[yellow]Recomendación: Ejecuta el reseteo completo[/yellow]",
            title="❌ Error",
            border_style="red"
        ))
    except Exception as e:
        console.print(Panel(
            f"[red]Error al verificar API key:[/red]\n{str(e)}",
            title="❌ Error",
            border_style="red"
        ))

def show_security_tips():
    """Muestra consejos de seguridad."""
    console.print("\n")
    tips = Table(title="🔐 Consejos de Seguridad para API Keys", border_style="cyan")
    tips.add_column("Tip", style="yellow", width=5)
    tips.add_column("Descripción", style="white")
    
    security_tips = [
        ("1", "❌ NUNCA compartas tu API key en chats, foros o GitHub"),
        ("2", "✅ Usa variables de entorno para almacenar keys"),
        ("3", "✅ Añade archivos .env a .gitignore"),
        ("4", "✅ Rota tus API keys periódicamente"),
        ("5", "✅ Revoca inmediatamente keys comprometidas"),
        ("6", "✅ Usa diferentes keys para dev/test/prod"),
        ("7", "❌ No incluyas keys en código fuente"),
        ("8", "✅ Monitorea el uso de tus API keys"),
    ]
    
    for tip_num, tip_text in security_tips:
        tips.add_row(tip_num, tip_text)
    
    console.print(tips)

if __name__ == "__main__":
    try:
        check_api_key_status()
        show_security_tips()
        
        console.print("\n")
        console.print(Panel(
            "[bold cyan]¿Necesitas resetear tu API key?[/bold cyan]\n\n"
            "Ejecuta: [bold green]run_reset.bat[/bold green]\n"
            "O: [bold green]python windsurf_reset.py[/bold green]",
            title="💡 Siguiente Paso",
            border_style="cyan"
        ))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Verificación cancelada por el usuario[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error inesperado: {str(e)}[/red]")
