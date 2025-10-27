"""
Script automatizado para configurar y subir el proyecto a GitHub
"""
import os
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text

console = Console()

def run_command(command: str, check: bool = True) -> tuple:
    """Ejecuta un comando y retorna el resultado."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return True, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_git_installed():
    """Verifica si Git está instalado."""
    console.print("\n[cyan]🔍 Verificando Git...[/cyan]")
    success, stdout, _ = run_command("git --version", check=False)
    
    if success:
        version = stdout.strip()
        console.print(f"[green]✅ Git instalado: {version}[/green]")
        return True
    else:
        console.print("[red]❌ Git no está instalado[/red]")
        console.print("[yellow]Descarga Git de: https://git-scm.com/downloads[/yellow]")
        return False

def check_git_config():
    """Verifica la configuración de Git."""
    console.print("\n[cyan]🔍 Verificando configuración de Git...[/cyan]")
    
    success, name, _ = run_command("git config --global user.name", check=False)
    success2, email, _ = run_command("git config --global user.email", check=False)
    
    if success and success2 and name.strip() and email.strip():
        console.print(f"[green]✅ Git configurado:[/green]")
        console.print(f"   Nombre: {name.strip()}")
        console.print(f"   Email: {email.strip()}")
        return True
    else:
        console.print("[yellow]⚠️  Git no está configurado completamente[/yellow]")
        
        if Confirm.ask("¿Deseas configurar Git ahora?"):
            name = Prompt.ask("Ingresa tu nombre")
            email = Prompt.ask("Ingresa tu email")
            
            run_command(f'git config --global user.name "{name}"')
            run_command(f'git config --global user.email "{email}"')
            
            console.print("[green]✅ Git configurado correctamente[/green]")
            return True
        return False

def init_repository():
    """Inicializa el repositorio Git."""
    console.print("\n[cyan]🔧 Inicializando repositorio Git...[/cyan]")
    
    if Path(".git").exists():
        console.print("[yellow]⚠️  El repositorio ya está inicializado[/yellow]")
        return True
    
    success, _, _ = run_command("git init")
    if success:
        console.print("[green]✅ Repositorio inicializado[/green]")
        
        # Cambiar a rama main
        run_command("git branch -M main")
        console.print("[green]✅ Rama principal: main[/green]")
        return True
    else:
        console.print("[red]❌ Error al inicializar repositorio[/red]")
        return False

def prepare_readme():
    """Prepara el README principal para GitHub."""
    console.print("\n[cyan]📝 Preparando README...[/cyan]")
    
    readme_github = Path("README_GITHUB.md")
    readme_main = Path("README.md")
    
    if readme_github.exists():
        # Hacer backup del README.md actual si existe
        if readme_main.exists():
            backup_name = "README_INDEX.md"
            readme_main.rename(backup_name)
            console.print(f"[yellow]📦 Backup creado: {backup_name}[/yellow]")
        
        # Renombrar README_GITHUB.md a README.md
        readme_github.rename("README.md")
        console.print("[green]✅ README.md preparado para GitHub[/green]")
        return True
    else:
        console.print("[yellow]⚠️  README_GITHUB.md no encontrado[/yellow]")
        return False

def update_readme_urls():
    """Actualiza las URLs en el README con el nombre de usuario de GitHub."""
    console.print("\n[cyan]🔗 Actualizando URLs en README...[/cyan]")
    
    github_user = Prompt.ask("Ingresa tu nombre de usuario de GitHub")
    repo_name = Prompt.ask("Ingresa el nombre del repositorio", default="windsurf-reset-tool")
    
    readme = Path("README.md")
    if readme.exists():
        content = readme.read_text(encoding='utf-8')
        
        # Reemplazar URLs
        content = content.replace("yourusername", github_user)
        content = content.replace("USUARIO_ORIGINAL", github_user)
        content = content.replace("TU_USUARIO", github_user)
        
        readme.write_text(content, encoding='utf-8')
        console.print(f"[green]✅ URLs actualizadas:[/green]")
        console.print(f"   Usuario: {github_user}")
        console.print(f"   Repo: {repo_name}")
        
        return github_user, repo_name
    else:
        console.print("[red]❌ README.md no encontrado[/red]")
        return None, None

def create_gitignore():
    """Verifica que .gitignore existe."""
    console.print("\n[cyan]📄 Verificando .gitignore...[/cyan]")
    
    gitignore = Path(".gitignore")
    if gitignore.exists():
        console.print("[green]✅ .gitignore encontrado[/green]")
        return True
    else:
        console.print("[yellow]⚠️  .gitignore no encontrado[/yellow]")
        return False

def add_remote(github_user: str, repo_name: str):
    """Agrega el repositorio remoto."""
    console.print("\n[cyan]🌐 Configurando repositorio remoto...[/cyan]")
    
    # Verificar si ya existe
    success, stdout, _ = run_command("git remote -v", check=False)
    if "origin" in stdout:
        console.print("[yellow]⚠️  Remote 'origin' ya existe[/yellow]")
        
        if Confirm.ask("¿Deseas reemplazarlo?"):
            run_command("git remote remove origin")
        else:
            return True
    
    # Agregar remote
    remote_url = f"https://github.com/{github_user}/{repo_name}.git"
    success, _, _ = run_command(f'git remote add origin {remote_url}')
    
    if success:
        console.print(f"[green]✅ Remote configurado:[/green]")
        console.print(f"   {remote_url}")
        return True
    else:
        console.print("[red]❌ Error al configurar remote[/red]")
        return False

def create_initial_commit():
    """Crea el commit inicial."""
    console.print("\n[cyan]💾 Creando commit inicial...[/cyan]")
    
    # Agregar todos los archivos
    console.print("   Agregando archivos...")
    run_command("git add .")
    
    # Ver archivos agregados
    success, stdout, _ = run_command("git status --short")
    if stdout:
        lines = stdout.strip().split('\n')
        console.print(f"[cyan]   {len(lines)} archivos agregados[/cyan]")
    
    # Crear commit
    commit_message = """Initial commit: Windsurf Reset Tool v2.0.0

- Complete reset functionality for Windsurf device IDs
- Deep cleaning of 15+ file types (cookies, cache, sessions)
- Automatic process detection and closing
- Complete test suite (test, simulate, verify)
- Comprehensive Spanish documentation
- Quick start batch scripts for Windows
- Automatic backups with timestamp
- Cross-platform support (Windows, macOS, Linux)
- Educational purpose project"""
    
    success, _, _ = run_command(f'git commit -m "{commit_message}"')
    
    if success:
        console.print("[green]✅ Commit inicial creado[/green]")
        return True
    else:
        console.print("[red]❌ Error al crear commit[/red]")
        return False

def push_to_github():
    """Sube el proyecto a GitHub."""
    console.print("\n[cyan]🚀 Subiendo a GitHub...[/cyan]")
    
    console.print("[yellow]⚠️  Asegúrate de haber creado el repositorio en GitHub primero[/yellow]")
    console.print("[yellow]   (https://github.com/new)[/yellow]")
    
    if not Confirm.ask("\n¿El repositorio ya está creado en GitHub?"):
        console.print("[yellow]Por favor, crea el repositorio primero y vuelve a ejecutar este paso[/yellow]")
        return False
    
    # Push
    console.print("\n[cyan]Subiendo archivos (esto puede tardar un momento)...[/cyan]")
    success, stdout, stderr = run_command("git push -u origin main", check=False)
    
    if success:
        console.print("[green]✅ Proyecto subido exitosamente a GitHub![/green]")
        return True
    else:
        console.print("[yellow]⚠️  Error al hacer push:[/yellow]")
        console.print(f"[red]{stderr}[/red]")
        
        if "authentication" in stderr.lower() or "permission" in stderr.lower():
            console.print("\n[yellow]💡 Sugerencias:[/yellow]")
            console.print("   1. Usa un Personal Access Token como contraseña")
            console.print("   2. Genera uno en: GitHub → Settings → Developer settings → Personal access tokens")
            console.print("   3. O configura SSH: https://docs.github.com/en/authentication/connecting-to-github-with-ssh")
        
        return False

def create_tag():
    """Crea y sube el tag de versión."""
    console.print("\n[cyan]🏷️  Creando tag de versión...[/cyan]")
    
    from version import __version__
    
    tag_name = f"v{__version__}"
    tag_message = f"Release {tag_name} - Complete Reset Tool"
    
    # Crear tag
    success, _, _ = run_command(f'git tag -a {tag_name} -m "{tag_message}"')
    
    if success:
        console.print(f"[green]✅ Tag creado: {tag_name}[/green]")
        
        # Push tag
        if Confirm.ask("¿Deseas subir el tag ahora?"):
            success, _, _ = run_command(f"git push origin {tag_name}")
            if success:
                console.print(f"[green]✅ Tag subido a GitHub[/green]")
                return True
        return True
    else:
        console.print("[yellow]⚠️  Error al crear tag (puede que ya exista)[/yellow]")
        return False

def print_next_steps(github_user: str, repo_name: str):
    """Imprime los siguientes pasos."""
    console.print("\n" + "="*60)
    console.print(Panel(
        Text(
            "¡PROYECTO SUBIDO EXITOSAMENTE A GITHUB!\n\n"
            "Próximos pasos opcionales:",
            justify="center"
        ),
        title="✅ Completado",
        border_style="green"
    ))
    
    repo_url = f"https://github.com/{github_user}/{repo_name}"
    
    console.print(f"""
🌐 Tu repositorio:
   {repo_url}

📝 Siguientes pasos:

1. Ver tu repositorio en GitHub:
   {repo_url}

2. Crear un Release (opcional):
   {repo_url}/releases/new
   - Selecciona el tag v2.0.0
   - Agrega descripción del release

3. Configurar el repositorio:
   - Agregar Topics: python, windsurf, educational, automation
   - Actualizar descripción en "About"
   - Habilitar Issues y Discussions

4. Compartir tu proyecto:
   - Link directo: {repo_url}
   - Clonar: git clone {repo_url}.git

5. Para futuras actualizaciones:
   - git add .
   - git commit -m "tu mensaje"
   - git push origin main

6. Para actualizar versión:
   - python update_version.py

📚 Documentación:
   - GITHUB_SETUP.md - Guía completa de configuración
   - CONTRIBUTING.md - Guía para contribuidores
   - update_version.py - Actualizar versión automáticamente
""")

def main():
    """Función principal."""
    console.clear()
    
    console.print(Panel(
        Text(
            "CONFIGURACIÓN AUTOMÁTICA DE GITHUB\n\n"
            "Este script te ayudará a:\n"
            "• Inicializar el repositorio Git\n"
            "• Preparar archivos para GitHub\n"
            "• Crear commit inicial\n"
            "• Subir proyecto a GitHub\n"
            "• Crear tags de versión",
            justify="center"
        ),
        title="🚀 Windsurf Reset Tool - Setup GitHub",
        border_style="cyan"
    ))
    
    # Paso 1: Verificar Git
    if not check_git_installed():
        return
    
    # Paso 2: Configurar Git
    if not check_git_config():
        console.print("\n[red]Git debe estar configurado para continuar[/red]")
        return
    
    # Paso 3: Inicializar repositorio
    if not init_repository():
        return
    
    # Paso 4: Preparar README
    prepare_readme()
    
    # Paso 5: Actualizar URLs
    github_user, repo_name = update_readme_urls()
    if not github_user:
        return
    
    # Paso 6: Verificar .gitignore
    create_gitignore()
    
    # Paso 7: Agregar remote
    if not add_remote(github_user, repo_name):
        return
    
    # Paso 8: Crear commit inicial
    if not create_initial_commit():
        return
    
    # Paso 9: Push a GitHub
    if not push_to_github():
        console.print("\n[yellow]⚠️  No se pudo subir a GitHub automáticamente[/yellow]")
        console.print("[cyan]Puedes intentar manualmente:[/cyan]")
        console.print("   git push -u origin main")
        
        if not Confirm.ask("\n¿Continuar con la configuración de tags?"):
            return
    
    # Paso 10: Crear tag
    create_tag()
    
    # Paso 11: Mostrar siguientes pasos
    print_next_steps(github_user, repo_name)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]❌ Proceso cancelado por el usuario[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Error: {str(e)}[/red]")
        sys.exit(1)
