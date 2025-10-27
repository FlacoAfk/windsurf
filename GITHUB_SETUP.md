# 🚀 Guía para Subir el Proyecto a GitHub

Esta guía te ayudará a crear un nuevo repositorio en GitHub y subir este proyecto paso a paso.

## 📋 Requisitos Previos

- ✅ Git instalado ([Descargar Git](https://git-scm.com/downloads))
- ✅ Cuenta de GitHub ([Crear cuenta](https://github.com/join))
- ✅ Git configurado con tu nombre y email

```bash
# Verificar si Git está instalado
git --version

# Configurar Git (si no lo has hecho)
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

## 🎯 Paso 1: Crear Repositorio en GitHub

### Opción A: Desde la Web (Recomendado)

1. Ve a [GitHub](https://github.com)
2. Haz click en el botón **"+"** (arriba a la derecha)
3. Selecciona **"New repository"**
4. Llena la información:
   - **Repository name**: `windsurf-reset-tool` (o el nombre que prefieras)
   - **Description**: `🔧 Educational tool to study desktop app state management and data persistence through Windsurf device ID reset`
   - **Visibility**: 
     - ✅ **Public** (recomendado para proyectos educativos)
     - ⚠️ Private (si prefieres mantenerlo privado)
   - **NO** inicialices con README, .gitignore o LICENSE (ya los tenemos)
5. Click en **"Create repository"**

### Opción B: Usando GitHub CLI

```bash
# Instalar GitHub CLI: https://cli.github.com/
gh repo create windsurf-reset-tool --public --source=. --remote=origin
```

## 🔧 Paso 2: Preparar el Proyecto Local

### A. Inicializar Git en el Proyecto

```bash
# Navegar a la carpeta del proyecto
cd c:\Users\elkaw\Desktop\windsurd

# Inicializar repositorio Git
git init

# Verificar estado
git status
```

### B. Configurar el Repositorio Remoto

Copia la URL de tu repositorio de GitHub (aparece después de crearlo):
```
https://github.com/TU_USUARIO/windsurf-reset-tool.git
```

Luego ejecuta:

```bash
# Agregar repositorio remoto
git remote add origin https://github.com/TU_USUARIO/windsurf-reset-tool.git

# Verificar que se agregó correctamente
git remote -v
```

### C. Cambiar Nombre del README Principal

```bash
# Renombrar README_GITHUB.md a README.md para GitHub
# (Puedes hacerlo manualmente o con este comando)

# Windows PowerShell:
Move-Item README_GITHUB.md README.md -Force

# O manualmente:
# 1. Elimina el README.md actual (el índice corto)
# 2. Renombra README_GITHUB.md a README.md
```

### D. Actualizar URLs en README.md

Abre `README.md` y reemplaza:
- `yourusername` → Tu nombre de usuario de GitHub
- `windsurf-reset-tool` → El nombre de tu repositorio (si es diferente)

Busca y reemplaza en estos lugares:
```markdown
https://github.com/yourusername/windsurf-reset-tool
```

## 📦 Paso 3: Crear el Primer Commit

```bash
# Agregar todos los archivos
git add .

# Verificar qué se agregará
git status

# Crear el primer commit
git commit -m "Initial commit: Windsurf Reset Tool v2.0.0

- Complete reset functionality for Windsurf device IDs
- Deep cleaning of 15+ file types (cookies, cache, sessions)
- Automatic process detection and closing
- Complete test suite (test, simulate, verify)
- Comprehensive Spanish documentation
- Quick start batch scripts for Windows
- Automatic backups with timestamp
- Cross-platform support (Windows, macOS, Linux)
- Educational purpose project"
```

## 🚀 Paso 4: Subir el Proyecto a GitHub

### Push Inicial

```bash
# Cambiar el nombre de la rama principal a 'main' (si es necesario)
git branch -M main

# Subir todo a GitHub
git push -u origin main
```

Si es la primera vez que usas Git con GitHub, te pedirá autenticación:

#### Autenticación con Token (Recomendado)

1. Ve a GitHub → Settings → Developer settings → Personal access tokens
2. Genera un token con permisos de `repo`
3. Usa el token como contraseña cuando Git te lo pida

#### O usa SSH

```bash
# Generar clave SSH (si no tienes)
ssh-keygen -t ed25519 -C "tu@email.com"

# Copiar clave pública
cat ~/.ssh/id_ed25519.pub

# Agregar en GitHub: Settings → SSH and GPG keys → New SSH key

# Cambiar URL remota a SSH
git remote set-url origin git@github.com:TU_USUARIO/windsurf-reset-tool.git
```

## 🏷️ Paso 5: Crear Tags y Releases

### Crear Tag de Versión

```bash
# Crear tag para v2.0.0
git tag -a v2.0.0 -m "Release v2.0.0 - Complete Reset Tool

Major features:
- Complete authentication reset
- Deep file cleaning
- Test suite
- Documentation
- Cross-platform support"

# Subir el tag
git push origin v2.0.0

# O subir todos los tags
git push origin --tags
```

### Crear Release en GitHub

1. Ve a tu repositorio en GitHub
2. Click en **"Releases"** (barra lateral derecha)
3. Click en **"Create a new release"**
4. Selecciona el tag `v2.0.0`
5. Título: `v2.0.0 - Complete Reset Tool`
6. Descripción:
   ```markdown
   ## 🎉 First Major Release

   ### ✨ Highlights
   - Complete Windsurf device ID and authentication reset
   - Deep cleaning of 15+ file types
   - Comprehensive test suite
   - Full Spanish documentation
   - Cross-platform support

   ### 📦 What's Included
   - Main reset script with backup functionality
   - Test suite (simulation, testing, verification)
   - Quick start batch scripts for Windows
   - Extensive documentation in Spanish
   - Educational purpose disclaimer

   ### 🚀 Quick Start
   ```bash
   pip install -r requirements.txt
   python simulate_reset.py  # Safe dry-run
   python windsurf_reset.py  # Actual reset
   ```

   See [README.md](README.md) for detailed instructions.
   ```
7. Click **"Publish release"**

## 📝 Paso 6: Configurar Información Adicional

### A. Agregar Topics al Repositorio

En GitHub:
1. Ve a tu repositorio
2. Click en ⚙️ (Settings) al lado de "About"
3. En "Topics", agrega:
   - `python`
   - `windsurf`
   - `reset-tool`
   - `educational`
   - `automation`
   - `desktop-apps`
   - `state-management`

### B. Actualizar Descripción

En la sección "About", agrega:
```
🔧 Educational tool to study desktop app state management through Windsurf reset functionality
```

Website: Deja vacío o agrega si tienes documentación online

### C. Habilitar Issues y Discussions

1. Settings → Features
2. ✅ Issues
3. ✅ Discussions (recomendado para proyecto educativo)

## 🔄 Paso 7: Mantener el Proyecto Actualizado

### Para Futuras Actualizaciones

```bash
# 1. Hacer cambios en los archivos

# 2. Ver qué cambió
git status
git diff

# 3. Agregar cambios
git add .

# 4. Commit con mensaje descriptivo
git commit -m "feat: Add nueva funcionalidad"

# 5. Push a GitHub
git push origin main

# 6. Si es una nueva versión, usa el script
python update_version.py
```

### Actualizar Versión Automáticamente

```bash
# Usar el script de actualización de versión
python update_version.py

# Seguir las instrucciones que muestra el script
```

## 📊 Paso 8: Crear GitHub Actions (Opcional)

Crear `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.7, 3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python test_script.py
```

## 🎯 Checklist Final

Antes de considerar el proyecto "publicado", verifica:

- [ ] ✅ Repositorio creado en GitHub
- [ ] ✅ Proyecto subido con `git push`
- [ ] ✅ README.md visible y formateado correctamente
- [ ] ✅ LICENSE presente
- [ ] ✅ .gitignore configurado
- [ ] ✅ Topics agregados
- [ ] ✅ Descripción actualizada
- [ ] ✅ Release v2.0.0 creada
- [ ] ✅ Tag v2.0.0 pusheado
- [ ] ✅ Issues habilitado
- [ ] ✅ URLs actualizadas en README.md

## 🎉 ¡Listo!

Tu proyecto ahora está en GitHub y listo para compartir:

```
https://github.com/TU_USUARIO/windsurf-reset-tool
```

### Compartir el Proyecto

Puedes compartir:
- El enlace directo del repositorio
- El enlace del release: `https://github.com/TU_USUARIO/windsurf-reset-tool/releases/tag/v2.0.0`

### Para Clonar tu Proyecto

Otros usuarios pueden clonar con:
```bash
git clone https://github.com/TU_USUARIO/windsurf-reset-tool.git
cd windsurf-reset-tool
pip install -r requirements.txt
```

## 📞 Solución de Problemas

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/windsurf-reset-tool.git
```

### Error: "failed to push some refs"
```bash
# Si el repositorio remoto tiene contenido
git pull origin main --allow-unrelated-histories
git push origin main
```

### Error de Autenticación
```bash
# Usar token personal en lugar de contraseña
# Generar en: GitHub → Settings → Developer settings → Personal access tokens
```

## 🔗 Enlaces Útiles

- [Guía de Git](https://git-scm.com/book/es/v2)
- [Guía de GitHub](https://guides.github.com/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Semantic Versioning](https://semver.org/)

---

**¡Tu proyecto educativo ahora está en GitHub!** 🎓✨
