# 🔧 Windsurf Reset Tool - Herramienta Mejorada

## 🎯 ¿Qué hace esta herramienta?

Esta herramienta **resetea completamente** tu instalación de Windsurf para permitirte crear nuevas cuentas gratuitas. Ahora incluye:

### ✅ Funcionalidades Mejoradas:

1. **Reseteo de IDs de dispositivo** (telemetry.machineId, telemetry.macMachineId, telemetry.devDeviceId)
2. **Limpieza de cookies y sesiones** - Elimina todos los datos de autenticación almacenados
3. **Eliminación de cache** - Borra archivos temporales que puedan contener información de sesión
4. **Limpieza de tokens API** - Remueve archivos que contienen API keys antiguas
5. **Reseteo de workspace storage** - Elimina configuraciones de espacios de trabajo
6. **Limpieza de logs** - Remueve archivos de registro que pueden contener tokens

## 🚀 Cómo usar

### Paso 0: Instalar dependencias
**PRIMERO:** Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

O instala manualmente:
```bash
pip install rich psutil
```

### Paso 1: Cerrar Windsurf
**IMPORTANTE:** Cierra completamente Windsurf antes de ejecutar esta herramienta.

**NOTA:** Si olvidas cerrar Windsurf, la herramienta te lo recordará y te ofrecerá cerrarlo automáticamente.

### Paso 2: Ejecutar el script
```bash
python windsurf_reset.py
```

### Paso 3: Seleccionar opción
Elige la opción `1` para resetear los identificadores del dispositivo.

### Paso 4: Confirmar
- El script te preguntará si quieres crear un backup (recomendado)
- Confirma que quieres continuar con el reseteo

### Paso 5: REINICIAR Windsurf
**MUY IMPORTANTE:** Después de ejecutar el script, debes reiniciar Windsurf completamente para que los cambios tengan efecto.

## 📁 Archivos que se eliminan

La herramienta limpia los siguientes directorios y archivos:

```
%APPDATA%\Windsurf\
├── Cookies (archivo de cookies)
├── Cookies-journal
├── Network Persistent State
├── Cache\ (directorio completo)
├── CachedData\ (directorio completo)
├── Code Cache\ (directorio completo)
├── GPUCache\ (directorio completo)
├── Session Storage\ (directorio completo)
├── Local Storage\ (directorio completo)
├── IndexedDB\ (directorio completo)
├── User\globalStorage\codeium.windsurf\ (directorio completo)
├── User\workspaceStorage\ (directorio completo)
└── logs\ (directorio completo)
```

## 🔑 ¿Por qué obtenías siempre la misma API key?

El problema anterior era que el script solo cambiaba los IDs de telemetría en `storage.json`, pero **NO eliminaba**:

- Los tokens de autenticación almacenados en cookies
- Las sesiones activas en "Session Storage"
- Los datos de usuario en "Local Storage"
- La información de workspace que contiene la API key

Ahora la herramienta limpia **TODOS** estos archivos, forzando a Windsurf a generar una nueva API key cuando inicies sesión nuevamente.

## ⚠️ Advertencias

1. **Perderás todas tus configuraciones**: El reseteo elimina workspace storage, así que perderás configuraciones de proyectos.
2. **Debes cerrar Windsurf completamente**: Si Windsurf está abierto, no funcionará correctamente.
3. **Crea un backup**: La herramienta te preguntará si quieres hacer backup - se recomienda hacerlo.
4. **Reinicia después del reseteo**: Los cambios solo se aplicarán después de reiniciar Windsurf.

## 🛠️ Requisitos

### Software necesario:
- Python 3.7 o superior

### Dependencias de Python:
Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

O manualmente:
```bash
pip install rich psutil
```

**Descripción de las dependencias:**
- `rich`: Interfaz de usuario mejorada con colores y barras de progreso
- `psutil`: Detección y cierre automático de procesos de Windsurf (recomendado)

## 📝 Notas adicionales

- La herramienta es compatible con Windows, macOS y Linux
- Genera nuevos UUIDs aleatorios para cada reseteo
- Muestra información detallada del proceso con barras de progreso
- Crea backups automáticos con timestamp si lo solicitas

## 💡 Solución de problemas

### Si sigues obteniendo la misma API key:

1. Verifica que Windsurf esté completamente cerrado (revisa el Task Manager)
2. Ejecuta el script como administrador (click derecho → "Ejecutar como administrador")
3. Asegúrate de REINICIAR Windsurf después del reseteo
4. Si el problema persiste, intenta desinstalar y reinstalar Windsurf después de ejecutar el script

### Error de permisos:

Si obtienes un error de permisos, ejecuta:
```bash
# Windows (PowerShell como administrador)
python windsurf_reset.py
```

## 📞 Soporte

Si tienes problemas:
1. Revisa que todas las dependencias estén instaladas
2. Verifica que tienes permisos de escritura en el directorio de Windsurf
3. Asegúrate de cerrar completamente Windsurf antes de ejecutar el script
