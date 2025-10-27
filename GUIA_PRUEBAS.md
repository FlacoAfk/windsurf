# 🧪 GUÍA DE PRUEBAS - Windsurf Reset Tool

## 📋 Descripción General

Antes de ejecutar el reseteo real, puedes usar estos scripts de prueba para **verificar que todo funcionará correctamente** sin hacer ningún cambio destructivo.

---

## 🎯 3 Niveles de Verificación

### 1️⃣ SIMULACIÓN (Dry-Run) - **EMPIEZA AQUÍ**
**Archivo:** `simulate_reset.py`  
**Script rápido:** `run_simulation.bat`

**Qué hace:**
- ✅ Muestra EXACTAMENTE qué hará el script
- ✅ Lista todos los archivos que se eliminarán
- ✅ Muestra cuánto espacio se liberará
- ✅ Indica qué claves se modificarán en storage.json
- ✅ Genera ejemplos de los nuevos IDs
- ✅ **100% SEGURO - No hace ningún cambio**

**Cómo ejecutar:**
```bash
# Opción A - Automática (doble click)
run_simulation.bat

# Opción B - Manual
python simulate_reset.py
```

**Cuándo usar:**
- 🎯 **SIEMPRE ejecuta esto PRIMERO**
- Antes de hacer el reseteo real
- Para ver qué archivos existen en tu sistema
- Para verificar cuánto espacio se liberará

---

### 2️⃣ PRUEBAS INTENSIVAS - **Para verificación profunda**
**Archivo:** `test_script.py`  
**Script rápido:** `run_tests.bat`

**Qué prueba:**
- ✅ Todas las dependencias (rich, psutil)
- ✅ Rutas de Windsurf (Windows/Mac/Linux)
- ✅ Permisos de escritura
- ✅ Archivos existentes y tamaños
- ✅ Procesos de Windsurf en ejecución
- ✅ Formato de storage.json
- ✅ Generación de UUIDs únicos

**Cómo ejecutar:**
```bash
# Opción A - Automática (doble click)
run_tests.bat

# Opción B - Manual
python test_script.py
```

**Cuándo usar:**
- Si tienes dudas sobre la configuración
- Para diagnosticar problemas
- Para verificar que todas las dependencias están instaladas
- Para ver un reporte detallado de tu instalación

---

### 3️⃣ VERIFICACIÓN DE PROCESOS - **Check específico**
**Archivo:** `check_windsurf.py`

**Qué hace:**
- ✅ Detecta si Windsurf está ejecutándose
- ✅ Muestra PID y uso de memoria
- ✅ Puede cerrar procesos automáticamente

**Cómo ejecutar:**
```bash
python check_windsurf.py
```

**Cuándo usar:**
- Antes de ejecutar el reseteo
- Si no estás seguro si Windsurf está cerrado
- Para verificar manualmente los procesos

---

## 🚀 FLUJO RECOMENDADO

```
┌─────────────────────────────────────────┐
│  PASO 1: Ejecutar SIMULACIÓN           │
│  run_simulation.bat                     │
│                                         │
│  → Revisa qué archivos se eliminarán   │
│  → Verifica el espacio a liberar       │
│  → Confirma que todo se ve correcto    │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  PASO 2: Ejecutar PRUEBAS INTENSIVAS   │
│  run_tests.bat                          │
│                                         │
│  → Verifica que todas las pruebas       │
│    pasen correctamente                  │
│  → Si alguna falla, revisa el error     │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  PASO 3: Ejecutar RESETEO REAL         │
│  run_reset.bat                          │
│                                         │
│  → Ahora sí hace los cambios reales    │
│  → Sigue las instrucciones del script  │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  PASO 4: REINICIAR WINDSURF            │
│                                         │
│  → MUY IMPORTANTE                       │
│  → Los cambios se aplican al reiniciar │
└─────────────────────────────────────────┘
```

---

## 📊 COMPARACIÓN DE HERRAMIENTAS

| Característica | Simulación | Pruebas | Check | Reseteo Real |
|----------------|-----------|---------|-------|--------------|
| **Hace cambios** | ❌ No | ❌ No | ❌ No | ✅ Sí |
| **Es seguro** | ✅ 100% | ✅ 100% | ✅ 100% | ⚠️ Permanente |
| **Muestra archivos** | ✅ Sí | ✅ Sí | ❌ No | ✅ Sí |
| **Verifica dependencias** | ❌ No | ✅ Sí | ❌ No | ⚠️ Requiere |
| **Cierra Windsurf** | ❌ No | ❌ No | ✅ Puede | ✅ Puede |
| **Genera nuevos IDs** | ✅ Ejemplo | ✅ Prueba | ❌ No | ✅ Reales |
| **Tiempo de ejecución** | ~10 seg | ~15 seg | ~5 seg | ~20 seg |

---

## 📋 EJEMPLOS DE SALIDA

### Simulación (Dry-Run)
```
═══ PASO 1: LIMPIEZA DE ARCHIVOS ═══

Archivos/Directorios a Eliminar
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Acción    ┃ Ruta              ┃ Estado      ┃ Efecto         ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ 🗑️ ELIMINAR │ Cookies           │ ✅ Existe   │ Liberará 45 KB │
│ 🗑️ ELIMINAR │ Cache             │ ✅ Existe   │ Liberará 2.3MB │
│ 🗑️ ELIMINAR │ Local Storage     │ ✅ Existe   │ Liberará 128KB │
│ ⏭️ OMITIR   │ logs              │ ❌ No existe│ Sin efecto     │
└───────────┴───────────────────┴─────────────┴────────────────┘

📊 Resumen de limpieza:
   • Se eliminarán: 12 archivos/directorios
   • Espacio a liberar: 15.7 MB
   • Se omitirán: 3 (no existen)
```

### Pruebas Intensivas
```
PRUEBA 1: Verificando imports y dependencias
═══════════════════════════════════════════════
✅ Todos los imports básicos funcionan correctamente
✅ psutil está instalado (detección de procesos habilitada)

PRUEBA 2: Verificando rutas de Windsurf
═══════════════════════════════════════════════
Sistema operativo: Windows
✅ Ruta base detectada: C:\Users\Usuario\AppData\Roaming
✅ La ruta base existe
✅ Directorio de Windsurf encontrado
✅ storage.json existe
✅ storage.json es válido (tiene 47 claves)
✅ Tienes permisos de escritura

RESUMEN DE PRUEBAS
═══════════════════════════════════════════════
Resultados de las Pruebas
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Prueba                  ┃ Resultado ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ Imports y Dependencias  │ ✅ PASÓ   │
│ Verificación de Rutas   │ ✅ PASÓ   │
│ Identificación          │ ✅ PASÓ   │
│ Detección de Procesos   │ ✅ PASÓ   │
│ Análisis de storage     │ ✅ PASÓ   │
│ Generación de IDs       │ ✅ PASÓ   │
└─────────────────────────┴───────────┘

📊 Total: 6 pruebas
✅ Pasadas: 6
❌ Falladas: 0

¡TODAS LAS PRUEBAS PASARON!
El script está listo para ejecutarse.
```

---

## ❓ PREGUNTAS FRECUENTES

### ¿Cuál debo ejecutar primero?
👉 **SIEMPRE empieza con la SIMULACIÓN** (`run_simulation.bat`)

### ¿Son seguras las pruebas?
👉 **SÍ, 100% seguras.** Ninguna prueba hace cambios permanentes.

### ¿Cuánto tiempo toman?
👉 Simulación: ~10 segundos  
👉 Pruebas: ~15 segundos  
👉 Total: menos de 1 minuto

### ¿Necesito ejecutar todas las pruebas?
👉 **Recomendado:** Simulación + Pruebas intensivas  
👉 **Mínimo:** Solo Simulación

### ¿Qué hago si una prueba falla?
👉 Lee el mensaje de error  
👉 Instala dependencias faltantes: `pip install -r requirements.txt`  
👉 Ejecuta como administrador si hay problemas de permisos  
👉 Revisa la documentación: `README_ES.md`

### ¿Las pruebas garantizan que funcionará?
👉 **Casi 100%.** Si todas las pruebas pasan, el reseteo funcionará correctamente.

---

## 🎯 CHECKLIST PRE-RESETEO

Antes de ejecutar el reseteo real, asegúrate de:

- [ ] ✅ Ejecutar `run_simulation.bat` y revisar la salida
- [ ] ✅ Ejecutar `run_tests.bat` y verificar que todas las pruebas pasen
- [ ] ✅ Cerrar Windsurf completamente (o dejar que el script lo cierre)
- [ ] ✅ Tener al menos 50 MB de espacio libre (para backups)
- [ ] ✅ Leer la salida de la simulación para saber qué esperar
- [ ] ✅ Anotar tus IDs actuales (si quieres compararlos después)

---

## 🚨 INTERPRETANDO RESULTADOS

### ✅ TODO BIEN - Puedes continuar
```
✅ Todas las pruebas pasaron
✅ Se encontraron archivos para limpiar
✅ storage.json existe y es válido
✅ Tienes permisos de escritura
```
👉 **Listo para ejecutar el reseteo real**

### ⚠️ ADVERTENCIAS - Revisa pero puedes continuar
```
⚠️ storage.json no existe (será creado)
⚠️ No hay archivos para limpiar (instalación nueva)
⚠️ psutil no está instalado (no se pueden detectar procesos)
```
👉 **No es crítico, pero revisa las advertencias**

### ❌ ERRORES - Debes corregir antes de continuar
```
❌ No tienes permisos de escritura
❌ Las dependencias no están instaladas
❌ El directorio base no existe
```
👉 **Corrige estos errores antes de ejecutar el reseteo**

---

## 📁 ARCHIVOS DE PRUEBA

| Archivo | Propósito | Seguro | Tiempo |
|---------|-----------|--------|--------|
| `simulate_reset.py` | Muestra qué hará sin hacerlo | ✅ Sí | ~10s |
| `test_script.py` | Pruebas exhaustivas del sistema | ✅ Sí | ~15s |
| `check_windsurf.py` | Verifica procesos activos | ✅ Sí | ~5s |
| `run_simulation.bat` | Ejecuta simulación (Windows) | ✅ Sí | ~10s |
| `run_tests.bat` | Ejecuta pruebas (Windows) | ✅ Sí | ~15s |

---

## 💡 TIPS ADICIONALES

### 1. Guarda la salida de las pruebas
```bash
python test_script.py > test_results.txt
python simulate_reset.py > simulation_results.txt
```

### 2. Ejecuta pruebas después del reseteo
```bash
# Después del reseteo, verifica los cambios:
python windsurf_reset.py
# Opción 2 → Ver configuración actual
# Verifica que los IDs sean diferentes
```

### 3. Compara antes y después
```bash
# ANTES del reseteo:
python simulate_reset.py > antes.txt

# DESPUÉS del reseteo:
python windsurf_reset.py (opción 2) > despues.txt

# Compara los archivos
```

---

## 🎉 RESUMEN

1. **Ejecuta `run_simulation.bat`** → Ve qué hará el script
2. **Ejecuta `run_tests.bat`** → Verifica que todo está listo
3. **Si todo pasa** → Ejecuta `run_reset.bat` (reseteo real)
4. **Reinicia Windsurf** → Los cambios se aplican al reiniciar

**¡Con estas pruebas puedes estar 100% seguro de que el reseteo funcionará!** 🚀

---

*Las pruebas te dan confianza. El reseteo te da una nueva API key.* ✨
