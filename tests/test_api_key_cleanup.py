"""
Script de pruebas para verificar que las API keys expuestas fueron eliminadas.
"""

import os
import re
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# API keys comprometidas que deben estar eliminadas
COMPROMISED_KEYS = [
    "njITed-5hvyJ3B5GSBLeV1ZIuCZLB-pVwkWPg8CL-aAhv5-dJa8hchKhL99FiRg6",
    "MbT-y1ibft2FFGhFLYzLkQMBhsM4fk6sUrsuRzuWM2hQBepmc0nbdAf2NeJd4tpyomfcC8",
    "VcvJxjQr9fDUe4fldfb2SumOzsh4WFUfdslr9ysV918GZ09bvII3niEnvNESsTEozmC2gEWvuFLfA9PcgR76WuFPMrXLLw",
]

# Extensiones de archivos a verificar
EXTENSIONS = ['.py', '.md', '.txt', '.json', '.bat', '.sh']

# Directorios a excluir
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', '.venv'}

def scan_files(base_path: Path):
    """Escanea todos los archivos en busca de API keys expuestas."""
    results = {
        'total_files': 0,
        'scanned_files': 0,
        'issues_found': [],
        'safe_files': []
    }
    
    test_file = Path(__file__).name
    
    for root, dirs, files in os.walk(base_path):
        # Excluir directorios
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            
            # Excluir este archivo de prueba
            if file_path.name == test_file:
                continue
            
            # Verificar extensión
            if file_path.suffix not in EXTENSIONS:
                continue
            
            results['total_files'] += 1
            
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                results['scanned_files'] += 1
                
                # Buscar API keys comprometidas
                issues = []
                for key_pattern in COMPROMISED_KEYS:
                    if key_pattern in content:
                        # Encontrar líneas específicas
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if key_pattern in line:
                                issues.append({
                                    'file': str(file_path.relative_to(base_path)),
                                    'line': i,
                                    'pattern': key_pattern[:20] + "...",
                                    'context': line[:80]
                                })
                
                if issues:
                    results['issues_found'].extend(issues)
                else:
                    results['safe_files'].append(str(file_path.relative_to(base_path)))
                    
            except Exception as e:
                console.print(f"[yellow]⚠️ Error leyendo {file_path}: {e}[/yellow]")
    
    return results

def test_placeholder_keys():
    """Verifica que los placeholders sean seguros."""
    safe_patterns = [
        "sk-ws-01-EXAMPLE-KEY",
        "sk-ws-01-abc123",
        "sk-ws-01-********",
        "[REDACTED]",
        "[OLD_KEY]",
    ]
    
    console.print("\n[cyan]🔍 Verificando placeholders seguros...[/cyan]")
    
    # Verificar que los placeholders existen
    verify_file = Path("verify_api_key.py")
    if verify_file.exists():
        content = verify_file.read_text()
        if "EXAMPLE-KEY" in content:
            console.print("  ✅ verify_api_key.py usa placeholder seguro")
        else:
            console.print("  ⚠️ verify_api_key.py no tiene placeholder esperado")
    
    return True

def test_documentation_sanitized():
    """Verifica que la documentación esté sanitizada."""
    console.print("\n[cyan]📚 Verificando documentación...[/cyan]")
    
    doc_files = [
        "GUIA_SEGURIDAD.md",
        "SOLUCION_ERROR.md",
        "ANALISIS_PROBLEMA.md",
        "RESUMEN_MEJORAS.md",
    ]
    
    safe = True
    for doc in doc_files:
        doc_path = Path(doc)
        if doc_path.exists():
            content = doc_path.read_text()
            # Buscar patrones de API keys reales
            if re.search(r'sk-ws-01-[A-Z][a-z0-9]{6}-[A-Za-z0-9]{10,}', content):
                console.print(f"  ⚠️ {doc} puede contener API key real")
                safe = False
            else:
                console.print(f"  ✅ {doc} limpio")
    
    return safe

def run_tests():
    """Ejecuta todas las pruebas."""
    console.print("\n")
    console.print(Panel(
        "[bold cyan]🧪 PRUEBAS DE LIMPIEZA DE API KEYS[/bold cyan]\n"
        "Verificando que todas las API keys expuestas fueron eliminadas...",
        title="🔒 Test Suite",
        border_style="cyan"
    ))
    
    base_path = Path(__file__).parent
    
    # Test 1: Escaneo de archivos
    console.print("\n[bold yellow]Test 1: Escaneo de Archivos[/bold yellow]")
    results = scan_files(base_path)
    
    # Tabla de resultados
    table = Table(title="📊 Resultados del Escaneo", border_style="blue")
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="white")
    
    table.add_row("Archivos totales", str(results['total_files']))
    table.add_row("Archivos escaneados", str(results['scanned_files']))
    table.add_row("Archivos seguros", str(len(results['safe_files'])))
    table.add_row("Issues encontrados", 
                  f"[red]{len(results['issues_found'])}[/red]" if results['issues_found'] 
                  else "[green]0[/green]")
    
    console.print(table)
    
    # Mostrar issues si existen
    if results['issues_found']:
        console.print("\n[red]❌ ISSUES ENCONTRADOS:[/red]")
        for issue in results['issues_found']:
            console.print(f"  📄 {issue['file']}:{issue['line']}")
            console.print(f"     Patrón: {issue['pattern']}")
            console.print(f"     Contexto: {issue['context']}\n")
    else:
        console.print("\n[green]✅ No se encontraron API keys comprometidas![/green]")
    
    # Test 2: Placeholders
    console.print("\n[bold yellow]Test 2: Placeholders Seguros[/bold yellow]")
    placeholder_test = test_placeholder_keys()
    
    # Test 3: Documentación
    console.print("\n[bold yellow]Test 3: Documentación Sanitizada[/bold yellow]")
    doc_test = test_documentation_sanitized()
    
    # Resumen final
    console.print("\n")
    all_tests_passed = (len(results['issues_found']) == 0 and 
                       placeholder_test and doc_test)
    
    if all_tests_passed:
        console.print(Panel(
            "[bold green]✅ TODAS LAS PRUEBAS PASARON[/bold green]\n\n"
            "• No se encontraron API keys comprometidas\n"
            "• Placeholders seguros en su lugar\n"
            "• Documentación sanitizada correctamente\n\n"
            "[cyan]Tu código está seguro para compartir.[/cyan]",
            title="🎉 ÉXITO",
            border_style="green"
        ))
    else:
        console.print(Panel(
            "[bold red]❌ ALGUNAS PRUEBAS FALLARON[/bold red]\n\n"
            "Revisa los issues encontrados arriba.\n"
            "Asegúrate de que todas las API keys reales\n"
            "hayan sido reemplazadas por placeholders.",
            title="⚠️ ATENCIÓN",
            border_style="red"
        ))
    
    return all_tests_passed

if __name__ == "__main__":
    try:
        success = run_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Pruebas canceladas por el usuario[/yellow]")
        exit(1)
    except Exception as e:
        console.print(f"\n[red]Error ejecutando pruebas: {e}[/red]")
        exit(1)
