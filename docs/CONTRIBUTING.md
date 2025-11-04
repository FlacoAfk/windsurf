# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Windsurf Reset Tool! Este es un proyecto educativo y damos la bienvenida a contribuciones de todos los niveles.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Guías de Estilo](#guías-de-estilo)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Configuración del Entorno](#configuración-del-entorno)

## 📜 Código de Conducta

Este proyecto está comprometido con proporcionar un ambiente acogedor e inclusivo para todos. Por favor, sé respetuoso y constructivo en todas las interacciones.

## 🎯 ¿Cómo Puedo Contribuir?

### Reportar Bugs

Si encuentras un bug, por favor crea un issue con:
- ✅ Descripción clara del problema
- ✅ Pasos para reproducir
- ✅ Comportamiento esperado vs. actual
- ✅ Sistema operativo y versión de Python
- ✅ Capturas de pantalla (si aplica)

**Template:**
```markdown
## Descripción
[Descripción clara del bug]

## Pasos para Reproducir
1. [Primer paso]
2. [Segundo paso]
3. [...]

## Comportamiento Esperado
[Lo que debería pasar]

## Comportamiento Actual
[Lo que realmente pasa]

## Entorno
- OS: [Windows 10/11, macOS, Linux]
- Python: [3.7, 3.8, 3.9, etc.]
- Versión del Tool: [2.0.0]
```

### Sugerir Mejoras

¿Tienes una idea para mejorar el proyecto? Crea un issue con:
- ✅ Descripción detallada de la mejora
- ✅ Por qué sería útil
- ✅ Posibles alternativas consideradas

### Contribuir Código

1. **Fork** el repositorio
2. **Crea una rama** para tu feature
3. **Haz tus cambios**
4. **Escribe/actualiza pruebas**
5. **Actualiza documentación**
6. **Envía un Pull Request**

## 🎨 Guías de Estilo

### Estilo de Código Python

Seguimos [PEP 8](https://pep8.org/) con algunas excepciones:

```python
# ✅ Bueno
def reset_windsurf_id() -> bool:
    """Resetea los identificadores de Windsurf."""
    try:
        storage_file = get_storage_file()
        # ...
        return True
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return False

# ❌ Malo
def resetWindsurfId():
    storage_file=get_storage_file()
    return True
```

### Convenciones de Nombres

- **Funciones**: `snake_case`
- **Clases**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Archivos**: `snake_case.py`

### Docstrings

Usa docstrings estilo Google:

```python
def function_name(param1: str, param2: int) -> bool:
    """Descripción breve de la función.

    Descripción más detallada si es necesaria.

    Args:
        param1: Descripción del primer parámetro.
        param2: Descripción del segundo parámetro.

    Returns:
        True si la operación fue exitosa, False en caso contrario.

    Raises:
        ValueError: Si param2 es negativo.
    """
    pass
```

### Commits

Usa mensajes de commit descriptivos siguiendo [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Tipos de commit
feat: Nueva funcionalidad
fix: Corrección de bug
docs: Cambios en documentación
style: Cambios de formato (no afectan código)
refactor: Refactorización de código
test: Añadir o modificar pruebas
chore: Tareas de mantenimiento

# Ejemplos
git commit -m "feat: Add macOS support for storage path detection"
git commit -m "fix: Handle missing storage.json file gracefully"
git commit -m "docs: Update installation instructions for Linux"
git commit -m "test: Add unit tests for backup functionality"
```

### Mensajes de Console (Rich)

Usa los estilos definidos en el proyecto:

```python
# ✅ Bueno
console.print("[green]✅ Operación exitosa[/green]")
console.print("[red]❌ Error detectado[/red]")
console.print("[yellow]⚠️  Advertencia[/yellow]")
console.print("[cyan]ℹ️  Información[/cyan]")

# ❌ Malo
print("Operación exitosa")
console.print("Error")
```

## 🔄 Proceso de Pull Request

### Antes de Enviar

1. **Actualiza tu fork** con la rama principal
2. **Ejecuta las pruebas**:
   ```bash
   python test_script.py
   ```
3. **Verifica el estilo**:
   ```bash
   # Si tienes flake8 instalado
   flake8 *.py
   ```
4. **Actualiza documentación** si añadiste features
5. **Actualiza CHANGELOG.md** con tus cambios

### Template de Pull Request

```markdown
## Descripción
[Descripción clara de los cambios]

## Tipo de Cambio
- [ ] Bug fix (cambio no breaking que arregla un issue)
- [ ] Nueva feature (cambio no breaking que añade funcionalidad)
- [ ] Breaking change (fix o feature que causaría que funcionalidad existente no funcione)
- [ ] Documentación

## ¿Cómo se ha probado?
[Describe las pruebas que ejecutaste]

## Checklist
- [ ] Mi código sigue las guías de estilo del proyecto
- [ ] He realizado una auto-revisión de mi código
- [ ] He comentado mi código en áreas difíciles de entender
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan nuevas advertencias
- [ ] He añadido pruebas que demuestran que mi fix funciona
- [ ] Todas las pruebas pasan localmente
- [ ] He actualizado el CHANGELOG.md
```

## 🛠️ Configuración del Entorno

### Setup Básico

```bash
# 1. Clonar tu fork
git clone https://github.com/TU_USUARIO/windsurf-reset-tool.git
cd windsurf-reset-tool

# 2. Añadir upstream remoto
git remote add upstream https://github.com/USUARIO_ORIGINAL/windsurf-reset-tool.git

# 3. Crear ambiente virtual
python -m venv venv

# 4. Activar ambiente virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Instalar dependencias de desarrollo (opcional)
pip install flake8 black pytest
```

### Flujo de Trabajo

```bash
# 1. Actualizar tu fork
git checkout main
git pull upstream main

# 2. Crear rama para tu feature
git checkout -b feature/mi-nueva-feature

# 3. Hacer cambios y commits
git add .
git commit -m "feat: Add nueva funcionalidad"

# 4. Push a tu fork
git push origin feature/mi-nueva-feature

# 5. Crear Pull Request en GitHub
```

## 🧪 Pruebas

### Ejecutar Pruebas

```bash
# Todas las pruebas
python test_script.py

# Simulación
python simulate_reset.py

# Verificación
python verify_changes.py
```

### Escribir Nuevas Pruebas

Si añades nueva funcionalidad, añade pruebas:

```python
def test_nueva_funcionalidad():
    """Prueba la nueva funcionalidad."""
    console.print("\n[bold cyan]PRUEBA X: Nueva Funcionalidad[/bold cyan]\n")
    
    try:
        resultado = mi_nueva_funcion()
        
        if resultado:
            console.print("[green]✅ Prueba pasada[/green]")
            return True
        else:
            console.print("[red]❌ Prueba fallida[/red]")
            return False
            
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        return False
```

## 📝 Documentación

### Actualizar Documentación

Si tu cambio afecta el uso del proyecto:

1. **README.md** - Si cambia la API principal
2. **GUIA_RAPIDA.md** - Si afecta el flujo de uso
3. **GUIA_PRUEBAS.md** - Si añades nuevas pruebas
4. **CHANGELOG.md** - Siempre documenta tus cambios

### Estilo de Documentación

- Usa emojis para claridad visual 📚
- Incluye ejemplos de código
- Mantén las secciones organizadas
- Usa bullet points para listas
- Incluye capturas si es relevante

## 🏷️ Versionamiento

Este proyecto usa [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Cambios incompatibles
- **MINOR** (0.X.0): Nueva funcionalidad compatible
- **PATCH** (0.0.X): Correcciones de bugs

Los maintainers actualizarán la versión al hacer releases.

## 🎓 Recursos para Contribuidores

### Python
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Rich Documentation](https://rich.readthedocs.io/)

### Git
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

### Testing
- [pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## ❓ ¿Preguntas?

Si tienes preguntas sobre cómo contribuir:

1. Revisa los [Issues existentes](https://github.com/USUARIO/windsurf-reset-tool/issues)
2. Abre un nuevo [Issue de pregunta](https://github.com/USUARIO/windsurf-reset-tool/issues/new)
3. Participa en [Discussions](https://github.com/USUARIO/windsurf-reset-tool/discussions)

## 🙏 Reconocimientos

¡Gracias por contribuir al proyecto! Todos los contribuidores serán reconocidos en el README.

---

**¿Listo para contribuir?** ¡Empieza con un [Good First Issue](https://github.com/USUARIO/windsurf-reset-tool/labels/good%20first%20issue)!
