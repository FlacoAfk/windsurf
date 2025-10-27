"""
Script para actualizar automáticamente la versión del proyecto.
Actualiza version.py, CHANGELOG.md y crea git tags.
"""
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple

def get_current_version() -> str:
    """Lee la versión actual de version.py."""
    version_file = Path(__file__).parent / "version.py"
    content = version_file.read_text(encoding='utf-8')
    match = re.search(r'__version__\s*=\s*"(\d+\.\d+\.\d+)"', content)
    if match:
        return match.group(1)
    raise ValueError("No se pudo encontrar la versión en version.py")

def parse_version(version: str) -> Tuple[int, int, int]:
    """Parsea una versión en formato MAJOR.MINOR.PATCH."""
    parts = version.split('.')
    return int(parts[0]), int(parts[1]), int(parts[2])

def bump_version(current: str, bump_type: str) -> str:
    """Incrementa la versión según el tipo de bump."""
    major, minor, patch = parse_version(current)
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Tipo de bump inválido: {bump_type}")

def update_version_file(new_version: str, changes: list):
    """Actualiza version.py con la nueva versión."""
    version_file = Path(__file__).parent / "version.py"
    content = version_file.read_text(encoding='utf-8')
    
    # Actualizar __version__
    content = re.sub(
        r'__version__\s*=\s*"[^"]+"',
        f'__version__ = "{new_version}"',
        content
    )
    
    # Actualizar VERSION_HISTORY
    today = datetime.now().strftime('%Y-%m-%d')
    bump_type = 'major' if new_version.endswith('.0.0') and not new_version.startswith('1.') else \
                'minor' if new_version.endswith('.0') else 'patch'
    
    new_entry = f'''    "{new_version}": {{
        "date": "{today}",
        "changes": {changes},
        "type": "{bump_type}"
    }},'''
    
    content = re.sub(
        r'(VERSION_HISTORY = \{)',
        f'\\1\n{new_entry}',
        content
    )
    
    version_file.write_text(content, encoding='utf-8')
    print(f"✅ version.py actualizado a v{new_version}")

def update_changelog(new_version: str, changes: list):
    """Actualiza CHANGELOG.md con la nueva versión."""
    changelog_file = Path(__file__).parent / "CHANGELOG.md"
    
    if not changelog_file.exists():
        print("⚠️  CHANGELOG.md no existe, creando uno nuevo")
        content = "# Changelog\n\n"
    else:
        content = changelog_file.read_text(encoding='utf-8')
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    new_entry = f"""## [{new_version}] - {today}

### Cambios
"""
    for change in changes:
        new_entry += f"- {change}\n"
    
    new_entry += "\n"
    
    # Insertar después del título
    content = re.sub(
        r'(# Changelog\n\n)',
        f'\\1{new_entry}',
        content
    )
    
    changelog_file.write_text(content, encoding='utf-8')
    print(f"✅ CHANGELOG.md actualizado")

def update_readme_badges(new_version: str):
    """Actualiza los badges de versión en README files."""
    readme_files = [
        Path(__file__).parent / "README_GITHUB.md",
        Path(__file__).parent / "README.md"
    ]
    
    for readme_file in readme_files:
        if readme_file.exists():
            content = readme_file.read_text(encoding='utf-8')
            content = re.sub(
                r'version-\d+\.\d+\.\d+-blue',
                f'version-{new_version}-blue',
                content
            )
            readme_file.write_text(content, encoding='utf-8')
            print(f"✅ {readme_file.name} actualizado")

def print_instructions(new_version: str):
    """Imprime instrucciones para completar el proceso."""
    print("\n" + "="*60)
    print("📝 SIGUIENTES PASOS:")
    print("="*60)
    print(f"""
1. Revisa los cambios:
   git diff

2. Haz commit de los cambios:
   git add version.py CHANGELOG.md README*.md
   git commit -m "chore: Bump version to {new_version}"

3. Crea un tag de git:
   git tag -a v{new_version} -m "Release version {new_version}"

4. Push los cambios y el tag:
   git push origin main
   git push origin v{new_version}

5. Crea un release en GitHub usando el tag v{new_version}
""")

def main():
    """Función principal."""
    print("🔧 Windsurf Reset Tool - Actualizador de Versión")
    print("="*60)
    
    # Obtener versión actual
    current_version = get_current_version()
    print(f"📌 Versión actual: {current_version}")
    
    # Pedir tipo de bump
    print("\n¿Qué tipo de actualización quieres hacer?")
    print("  1. PATCH (0.0.X) - Corrección de bugs")
    print("  2. MINOR (0.X.0) - Nueva funcionalidad compatible")
    print("  3. MAJOR (X.0.0) - Cambios incompatibles")
    
    choice = input("\nSelecciona (1/2/3): ").strip()
    
    bump_types = {'1': 'patch', '2': 'minor', '3': 'major'}
    if choice not in bump_types:
        print("❌ Opción inválida")
        sys.exit(1)
    
    bump_type = bump_types[choice]
    new_version = bump_version(current_version, bump_type)
    
    print(f"\n🆕 Nueva versión será: {new_version}")
    
    # Pedir cambios
    print("\nIngresa los cambios (uno por línea, línea vacía para terminar):")
    changes = []
    while True:
        change = input("  - ").strip()
        if not change:
            break
        changes.append(change)
    
    if not changes:
        print("⚠️  Debes ingresar al menos un cambio")
        sys.exit(1)
    
    # Confirmar
    print(f"\n📋 Resumen:")
    print(f"   Versión: {current_version} → {new_version}")
    print(f"   Tipo: {bump_type.upper()}")
    print(f"   Cambios: {len(changes)}")
    
    confirm = input("\n¿Proceder con la actualización? (s/n): ").strip().lower()
    if confirm != 's':
        print("❌ Actualización cancelada")
        sys.exit(0)
    
    # Actualizar archivos
    print("\n🔄 Actualizando archivos...")
    update_version_file(new_version, changes)
    update_changelog(new_version, changes)
    update_readme_badges(new_version)
    
    # Mostrar instrucciones
    print_instructions(new_version)
    
    print("✅ Actualización completada!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Actualización cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
