"""
Pruebas de seguridad exhaustivas para verificar limpieza de API keys.
Incluye verificación de snapshots, logs y archivos de respaldo.
"""

import os
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track

console = Console()

class SecurityScanner:
    """Escáner de seguridad para detectar API keys expuestas."""
    
    # Patrones de API keys reales comprometidas (fragmentos únicos)
    COMPROMISED_PATTERNS = [
        "njITed",
        "dJa8hchKhL99FiRg6",
        "MbT-y1ibft2FFGhFLYzLkQMBhsM4fk6sUrsuRzuWM2hQBepmc0nbdAf2",
        "VcvJxjQr9fDUe4fldfb2SumOzsh4WFUfdslr9ysV918GZ09bvII3niEnvNEsS",
    ]
    
    # Patrones seguros que NO deben generar alertas
    SAFE_PATTERNS = [
        "EXAMPLE-KEY",
        "abc123",
        "[REDACTED]",
        "[OLD_KEY]",
        "********",
    ]
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.results = {
            'files_scanned': 0,
            'vulnerable_files': [],
            'safe_files': [],
            'errors': [],
        }
    
    def is_safe_context(self, content: str, pattern: str) -> bool:
        """Verifica si el patrón aparece en un contexto seguro."""
        # Buscar líneas con el patrón
        lines = content.split('\n')
        for line in lines:
            if pattern in line:
                # Verificar si hay marcadores de seguridad cerca
                for safe in self.SAFE_PATTERNS:
                    if safe in line:
                        return True
                # Verificar si es un comentario explicativo
                if any(marker in line for marker in ['#', '//', '<!--', 'ejemplo', 'example']):
                    continue
                return False
        return True
    
    def scan_file(self, file_path: Path) -> dict:
        """Escanea un archivo individual."""
        try:
            # Leer contenido
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                content = json.dumps(data, indent=2)
            else:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Buscar patrones comprometidos
            vulnerabilities = []
            for pattern in self.COMPROMISED_PATTERNS:
                if pattern in content and not self.is_safe_context(content, pattern):
                    vulnerabilities.append(pattern)
            
            return {
                'file': str(file_path.relative_to(self.base_path)),
                'vulnerable': len(vulnerabilities) > 0,
                'patterns': vulnerabilities
            }
            
        except Exception as e:
            return {
                'file': str(file_path.relative_to(self.base_path)),
                'error': str(e)
            }
    
    def scan_directory(self, extensions=None):
        """Escanea todos los archivos relevantes."""
        if extensions is None:
            extensions = {'.py', '.md', '.txt', '.json', '.bat', '.sh', '.log'}
        
        # Excluir archivos de prueba
        exclude_files = {'test_api_key_cleanup.py', 'test_comprehensive_security.py'}
        
        files_to_scan = []
        for ext in extensions:
            for file_path in self.base_path.rglob(f'*{ext}'):
                if file_path.name not in exclude_files:
                    if not any(part.startswith('.') for part in file_path.parts):
                        files_to_scan.append(file_path)
        
        console.print(f"\n[cyan]Escaneando {len(files_to_scan)} archivos...[/cyan]")
        
        for file_path in track(files_to_scan, description="Escaneando"):
            result = self.scan_file(file_path)
            self.results['files_scanned'] += 1
            
            if 'error' in result:
                self.results['errors'].append(result)
            elif result['vulnerable']:
                self.results['vulnerable_files'].append(result)
            else:
                self.results['safe_files'].append(result['file'])
        
        return self.results

def test_snapshots():
    """Verifica que los snapshots no contengan API keys."""
    console.print("\n[bold yellow]Test Especial: Snapshots[/bold yellow]")
    
    snapshot_files = list(Path('.').glob('snapshot*.json'))
    
    if not snapshot_files:
        console.print("  ℹ️ No se encontraron archivos snapshot")
        return True
    
    all_safe = True
    for snapshot in snapshot_files:
        try:
            with open(snapshot, 'r') as f:
                data = json.load(f)
            
            # Verificar que no haya claves sospechosas
            content_str = json.dumps(data)
            has_api_key = 'api' in content_str.lower() and 'key' in content_str.lower()
            
            if has_api_key:
                console.print(f"  ⚠️ {snapshot.name} contiene referencias a API keys")
                all_safe = False
            else:
                console.print(f"  ✅ {snapshot.name} limpio")
        except Exception as e:
            console.print(f"  ❌ Error leyendo {snapshot.name}: {e}")
            all_safe = False
    
    return all_safe

def test_code_examples():
    """Verifica que los ejemplos de código usen placeholders seguros."""
    console.print("\n[bold yellow]Test: Ejemplos de Código[/bold yellow]")
    
    # Buscar archivos con ejemplos
    example_files = [
        'GUIA_SEGURIDAD.md',
        'COMO_USAR_MEJORAS.md',
        'MEJORAS_V2.1.md',
    ]
    
    all_safe = True
    for filename in example_files:
        filepath = Path(filename)
        if not filepath.exists():
            continue
        
        content = filepath.read_text()
        
        # Buscar bloques de código con API keys
        import re
        code_blocks = re.findall(r'```(?:python|bash)?\n(.*?)```', content, re.DOTALL)
        
        for block in code_blocks:
            if 'sk-ws-01' in block:
                # Verificar que sea un placeholder seguro
                if 'EXAMPLE' in block or 'abc123' in block or '***' in block:
                    continue
                else:
                    console.print(f"  ⚠️ {filename} tiene ejemplo con API key posiblemente real")
                    all_safe = False
                    break
        else:
            console.print(f"  ✅ {filename} ejemplos seguros")
    
    return all_safe

def run_comprehensive_tests():
    """Ejecuta suite completa de pruebas de seguridad."""
    console.print("\n")
    console.print(Panel(
        "[bold cyan]🔐 PRUEBAS DE SEGURIDAD EXHAUSTIVAS[/bold cyan]\n"
        "Verificación completa de limpieza de API keys\n"
        "Incluyendo código, documentación, snapshots y logs",
        title="🛡️ Security Test Suite",
        border_style="cyan"
    ))
    
    base_path = Path('.')
    
    # Test 1: Escaneo completo
    console.print("\n[bold yellow]Test 1: Escaneo Completo de Archivos[/bold yellow]")
    scanner = SecurityScanner(base_path)
    results = scanner.scan_directory()
    
    # Tabla de resultados
    table = Table(title="📊 Resultados del Escaneo", border_style="blue")
    table.add_column("Métrica", style="cyan", width=30)
    table.add_column("Valor", style="white", justify="right")
    
    table.add_row("Archivos escaneados", str(results['files_scanned']))
    table.add_row("Archivos seguros", f"[green]{len(results['safe_files'])}[/green]")
    table.add_row("Archivos vulnerables", 
                  f"[red]{len(results['vulnerable_files'])}[/red]" 
                  if results['vulnerable_files'] else "[green]0[/green]")
    table.add_row("Errores de lectura", str(len(results['errors'])))
    
    console.print(table)
    
    # Detalles de vulnerabilidades
    if results['vulnerable_files']:
        console.print("\n[red]❌ VULNERABILIDADES ENCONTRADAS:[/red]")
        for vuln in results['vulnerable_files']:
            console.print(f"\n  📄 [bold]{vuln['file']}[/bold]")
            console.print(f"     Patrones encontrados: {', '.join(vuln['patterns'])}")
    
    # Test 2: Snapshots
    snapshot_test = test_snapshots()
    
    # Test 3: Ejemplos de código
    code_test = test_code_examples()
    
    # Resumen final
    console.print("\n")
    all_passed = (len(results['vulnerable_files']) == 0 and 
                 snapshot_test and code_test)
    
    # Panel de resumen
    summary_table = Table(show_header=False, border_style="cyan")
    summary_table.add_column("Test", style="white")
    summary_table.add_column("Estado", justify="center")
    
    summary_table.add_row("Escaneo de archivos", 
                          "✅" if len(results['vulnerable_files']) == 0 else "❌")
    summary_table.add_row("Snapshots limpios", "✅" if snapshot_test else "❌")
    summary_table.add_row("Ejemplos seguros", "✅" if code_test else "❌")
    
    if all_passed:
        console.print(Panel(
            summary_table,
            title="[bold green]🎉 TODAS LAS PRUEBAS PASARON[/bold green]",
            subtitle="[cyan]Tu código es seguro para compartir públicamente[/cyan]",
            border_style="green"
        ))
    else:
        console.print(Panel(
            summary_table,
            title="[bold red]⚠️ ALGUNAS PRUEBAS FALLARON[/bold red]",
            subtitle="[yellow]Revisa los detalles arriba[/yellow]",
            border_style="red"
        ))
    
    return all_passed

if __name__ == "__main__":
    try:
        success = run_comprehensive_tests()
        console.print("\n")
        exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Pruebas canceladas[/yellow]")
        exit(1)
    except Exception as e:
        console.print(f"\n[red]Error crítico: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        exit(1)
