"""
Script de pruebas completo para todas las características v2.1
Verifica que todas las herramientas nuevas funcionen correctamente.
"""
import os
import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console(force_terminal=True, legacy_windows=False)


def run_test(name: str, command: list, should_pass: bool = True) -> dict:
    """
    Ejecuta un test y retorna resultado.
    
    Args:
        name: Nombre del test
        command: Comando a ejecutar
        should_pass: Si debe pasar (exit code 0)
    
    Returns:
        Dict con resultado del test
    """
    console.print(f"\n[cyan]🧪 Ejecutando:[/cyan] [bold]{name}[/bold]")
    
    try:
        # Agregar encoding UTF-8
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        
        passed = (result.returncode == 0) if should_pass else (result.returncode != 0)
        
        if passed:
            console.print(f"   [green]✅ PASÓ[/green] (exit code: {result.returncode})")
            return {'name': name, 'passed': True, 'error': None}
        else:
            console.print(f"   [red]❌ FALLÓ[/red] (exit code: {result.returncode})")
            if result.stderr:
                console.print(f"   [red]Error:[/red] {result.stderr[:200]}")
            return {'name': name, 'passed': False, 'error': result.stderr}
    
    except subprocess.TimeoutExpired:
        console.print(f"   [red]❌ TIMEOUT[/red] (>30s)")
        return {'name': name, 'passed': False, 'error': 'Timeout'}
    
    except Exception as e:
        console.print(f"   [red]❌ ERROR[/red]: {str(e)}")
        return {'name': name, 'passed': False, 'error': str(e)}


def check_file_exists(filepath: str) -> bool:
    """Verifica si un archivo existe."""
    exists = Path(filepath).exists()
    if exists:
        console.print(f"   [green]✅[/green] {filepath}")
    else:
        console.print(f"   [red]❌[/red] {filepath}")
    return exists


def main():
    """Función principal de pruebas."""
    console.clear()
    
    # Header
    console.print(Panel(
        Text("PRUEBAS COMPLETAS v2.1\nWindsurf Reset Tool", justify="center"),
        title="🧪 Test Suite Completo",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    results = []
    
    # ====== FASE 1: ARCHIVOS ESENCIALES ======
    console.print("\n" + "="*60)
    console.print("[bold cyan]FASE 1: Verificando Archivos Esenciales[/bold cyan]")
    console.print("="*60)
    
    essential_files = [
        "windsurf_reset.py",
        "api_key_extractor.py",
        "enhanced_logger.py",
        "post_reset_verify.py",
        "run_complete_check.bat",
        "requirements.txt",
        "test_script.py",
        "simulate_reset.py",
        "README.md",
        "GUIA_SEGURIDAD.md",
        "MEJORAS_V2.1.md",
        "COMO_USAR_MEJORAS.md",
        "CHANGELOG.md"
    ]
    
    files_ok = 0
    for file in essential_files:
        if check_file_exists(file):
            files_ok += 1
    
    results.append({
        'name': 'Archivos Esenciales',
        'passed': files_ok == len(essential_files),
        'error': None if files_ok == len(essential_files) else f"Faltan {len(essential_files) - files_ok} archivos"
    })
    
    # ====== FASE 2: IMPORTS Y DEPENDENCIAS ======
    console.print("\n" + "="*60)
    console.print("[bold cyan]FASE 2: Verificando Imports y Dependencias[/bold cyan]")
    console.print("="*60)
    
    test_imports = """
import json
import os
import shutil
import uuid
import platform
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
try:
    import psutil
    print("psutil: OK")
except:
    print("psutil: NO INSTALADO (opcional)")
print("Todos los imports básicos: OK")
"""
    
    result = run_test(
        "Imports Básicos",
        ["python", "-c", test_imports]
    )
    results.append(result)
    
    # ====== FASE 3: HERRAMIENTAS NUEVAS ======
    console.print("\n" + "="*60)
    console.print("[bold cyan]FASE 3: Probando Herramientas Nuevas v2.1[/bold cyan]")
    console.print("="*60)
    
    # Test 1: API Key Extractor (debe ejecutar sin errores)
    result = run_test(
        "API Key Extractor",
        ["python", "api_key_extractor.py"]
    )
    results.append(result)
    
    # Test 2: Enhanced Logger (ejemplo)
    result = run_test(
        "Enhanced Logger",
        ["python", "enhanced_logger.py"]
    )
    results.append(result)
    
    # Test 3: Post-Reset Verify
    result = run_test(
        "Post-Reset Verify",
        ["python", "post_reset_verify.py"]
    )
    results.append(result)
    
    # ====== FASE 4: SCRIPTS EXISTENTES ======
    console.print("\n" + "="*60)
    console.print("[bold cyan]FASE 4: Verificando Scripts Existentes[/bold cyan]")
    console.print("="*60)
    
    # Test suite original
    result = run_test(
        "Test Script Original",
        ["python", "test_script.py"]
    )
    results.append(result)
    
    # Simulación
    result = run_test(
        "Simulación de Reset",
        ["python", "simulate_reset.py"]
    )
    results.append(result)
    
    # ====== FASE 5: VALIDACIÓN DE CÓDIGO ======
    console.print("\n" + "="*60)
    console.print("[bold cyan]FASE 5: Validación de Código Principal[/bold cyan]")
    console.print("="*60)
    
    # Verificar sintaxis de windsurf_reset.py
    result = run_test(
        "Sintaxis windsurf_reset.py",
        ["python", "-m", "py_compile", "windsurf_reset.py"]
    )
    results.append(result)
    
    # Verificar que windsurf_reset.py tiene la nueva clase
    check_code = """
import windsurf_reset
assert hasattr(windsurf_reset, 'ResetStatistics'), "Falta clase ResetStatistics"
assert hasattr(windsurf_reset, 'reset_windsurf_id'), "Falta función reset_windsurf_id"
print("Código principal: OK")
"""
    result = run_test(
        "Validación de Clases Nuevas",
        ["python", "-c", check_code]
    )
    results.append(result)
    
    # ====== FASE 6: DOCUMENTACIÓN ======
    console.print("\n" + "="*60)
    console.print("[bold cyan]FASE 6: Verificando Documentación[/bold cyan]")
    console.print("="*60)
    
    docs = {
        "README.md": ["2.1.0", "API Key Extractor", "Enhanced Logger"],
        "GUIA_SEGURIDAD.md": ["enmascaramiento", "API key", "seguridad"],
        "MEJORAS_V2.1.md": ["v2.1", "nuevas características", "estadísticas"],
        "CHANGELOG.md": ["2.1.0", "Added", "Security"]
    }
    
    docs_ok = 0
    for doc, keywords in docs.items():
        if Path(doc).exists():
            content = Path(doc).read_text(encoding='utf-8')
            found_all = all(kw.lower() in content.lower() for kw in keywords)
            if found_all:
                console.print(f"   [green]✅[/green] {doc} - Contiene keywords esperadas")
                docs_ok += 1
            else:
                console.print(f"   [yellow]⚠️[/yellow] {doc} - Faltan algunas keywords")
        else:
            console.print(f"   [red]❌[/red] {doc} - No existe")
    
    results.append({
        'name': 'Documentación Completa',
        'passed': docs_ok == len(docs),
        'error': None if docs_ok == len(docs) else f"Documentación incompleta"
    })
    
    # ====== RESUMEN FINAL ======
    console.print("\n" + "="*70)
    console.print("[bold cyan]📊 RESUMEN FINAL DE PRUEBAS[/bold cyan]")
    console.print("="*70 + "\n")
    
    # Tabla de resultados
    table = Table(title="Resultados Detallados")
    table.add_column("Test", style="white", no_wrap=True)
    table.add_column("Resultado", style="bold")
    table.add_column("Detalles", style="dim")
    
    passed_count = 0
    failed_count = 0
    
    for result in results:
        if result['passed']:
            table.add_row(
                result['name'],
                "[green]✅ PASÓ[/green]",
                "-"
            )
            passed_count += 1
        else:
            error_msg = result['error'][:50] if result['error'] else "Error desconocido"
            table.add_row(
                result['name'],
                "[red]❌ FALLÓ[/red]",
                error_msg
            )
            failed_count += 1
    
    console.print(table)
    
    # Estadísticas
    console.print(f"\n[cyan]📊 Total de pruebas:[/cyan] {len(results)}")
    console.print(f"[green]✅ Pasadas:[/green] {passed_count}")
    console.print(f"[red]❌ Falladas:[/red] {failed_count}")
    
    success_rate = (passed_count / len(results)) * 100 if results else 0
    console.print(f"[cyan]📈 Tasa de éxito:[/cyan] {success_rate:.1f}%")
    
    # Panel final
    if failed_count == 0:
        console.print("\n" + "="*70)
        console.print(Panel(
            Text(
                "🎉 ¡TODAS LAS PRUEBAS PASARON! 🎉\n\n"
                "✅ Archivos esenciales presentes\n"
                "✅ Todas las herramientas funcionan\n"
                "✅ Scripts existentes operativos\n"
                "✅ Código validado correctamente\n"
                "✅ Documentación completa\n\n"
                "El proyecto está listo para usar en producción.\n"
                "Ejecuta: run_complete_check.bat para comenzar",
                justify="center"
            ),
            title="[bold green]✅ ÉXITO TOTAL[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
    elif failed_count <= 2:
        console.print("\n" + "="*70)
        console.print(Panel(
            Text(
                f"⚠️  Algunas pruebas fallaron ({failed_count})\n\n"
                "El proyecto está mayormente funcional.\n"
                "Revisa los errores arriba para más detalles.",
                justify="center"
            ),
            title="[bold yellow]⚠️  ADVERTENCIA[/bold yellow]",
            border_style="yellow",
            padding=(1, 2)
        ))
    else:
        console.print("\n" + "="*70)
        console.print(Panel(
            Text(
                f"❌ Múltiples pruebas fallaron ({failed_count}/{len(results)})\n\n"
                "Revisa los errores antes de usar el proyecto.\n"
                "Verifica dependencias: pip install -r requirements.txt",
                justify="center"
            ),
            title="[bold red]❌ ERROR[/bold red]",
            border_style="red",
            padding=(1, 2)
        ))
    
    # Exit code
    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Pruebas canceladas por el usuario[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error fatal en suite de pruebas: {str(e)}[/red]")
        sys.exit(1)
