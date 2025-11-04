# 🔒 GUÍA DE SEGURIDAD - Windsurf Reset Tool

## 🎯 Propósito de Esta Guía

Esta guía te enseña cómo manejar información sensible (API keys, tokens) de forma segura al usar herramientas como Windsurf Reset Tool.

---

## ⚠️ REGLA DE ORO

> **NUNCA compartas API keys, tokens o credenciales completas públicamente.**

### ¿Por qué?

Una API key expuesta permite a otros:
- ✅ Usar tu cuenta
- ✅ Agotar tus créditos/límites
- ✅ Acceder a tus datos
- ✅ Hacer peticiones en tu nombre

---

## 🚨 SITUACIONES DE RIESGO

### ❌ NO Compartas API Keys En:

1. **Chats públicos**
   ```
   ❌ "Mi API key es: sk-ws-01-abc123..."
   ```

2. **Foros o Q&A**
   ```
   ❌ Stack Overflow, Reddit, Discord público
   ```

3. **Screenshots**
   ```
   ❌ Capturas de pantalla con keys visibles
   ```

4. **Código en GitHub**
   ```python
   ❌ API_KEY = "sk-ws-01-abc123..."  # Hard-coded
   ```

5. **Logs públicos**
   ```
   ❌ Logs en GitHub Actions, Travis CI, etc.
   ```

6. **Emails no encriptados**
   ```
   ❌ Enviar keys por email sin protección
   ```

---

## ✅ CÓMO COMPARTIR INFORMACIÓN SENSIBLE DE FORMA SEGURA

### 1. Enmascaramiento (Masking)

**Mostrar solo inicio y final:**

```
✅ BIEN:    sk-ws-01********YHQ
❌ MAL:     sk-ws-01-abc123def456ghi789jkl012mno345pqr678...
```

**Código de ejemplo:**
```python
def mask_api_key(api_key: str, visible: int = 8) -> str:
    """Enmascara API key mostrando solo inicio y final."""
    if len(api_key) <= visible * 2:
        return "***SHORT***"
    
    start = api_key[:visible]
    end = api_key[-visible:]
    middle = '*' * (len(api_key) - visible * 2)
    
    return f"{start}{middle}{end}"

# Uso
api_key = "sk-ws-01-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567"
print(mask_api_key(api_key))
# Output: sk-ws-01********z567
```

### 2. Redacción Completa

**Para información muy sensible:**

```
✅ BIEN:    ********
✅ BIEN:    [REDACTED]
✅ BIEN:    <API_KEY_OMITIDA>
❌ MAL:     sk-ws-01-abc123...
```

### 3. Uso de Variables de Entorno

**En lugar de hard-coding:**

```python
# ❌ MAL: Hard-coded en el código
API_KEY = "sk-ws-01-abc123..."

# ✅ BIEN: Variable de entorno
import os
API_KEY = os.getenv("WINDSURF_API_KEY")

if not API_KEY:
    raise ValueError("WINDSURF_API_KEY no está configurada")
```

**Configurar en Windows:**
```bash
# Temporal (solo sesión actual)
set WINDSURF_API_KEY=sk-ws-01-abc123...

# Permanente
setx WINDSURF_API_KEY "sk-ws-01-abc123..."
```

**Configurar en Linux/macOS:**
```bash
# Temporal
export WINDSURF_API_KEY="sk-ws-01-abc123..."

# Permanente (agregar a ~/.bashrc o ~/.zshrc)
echo 'export WINDSURF_API_KEY="sk-ws-01-abc123..."' >> ~/.bashrc
```

### 4. Archivos .env

**Crear archivo `.env`:**
```bash
# .env
WINDSURF_API_KEY=sk-ws-01-abc123...
ANOTHER_SECRET=my-secret-value
```

**Agregar a `.gitignore`:**
```bash
# .gitignore
.env
.env.local
.env.*.local
```

**Usar en Python:**
```python
# Instalar python-dotenv
# pip install python-dotenv

from dotenv import load_dotenv
import os

load_dotenv()  # Carga variables desde .env

API_KEY = os.getenv("WINDSURF_API_KEY")
```

---

## 🛡️ HERRAMIENTAS DE ESTE PROYECTO

### 1. API Key Extractor (Seguro)

Este proyecto incluye `api_key_extractor.py` que:

✅ **Enmascara automáticamente** las keys
✅ **No expone** información sensible completa
✅ **Te ayuda** a identificar qué está almacenado

**Uso seguro:**
```bash
python api_key_extractor.py
```

**Output seguro:**
```
Clave                     Valor Enmascarado           Longitud
────────────────────────────────────────────────────────────
codeium.api.token         sk-ws-01********YHQ        95
windsurf.session          sess_abc********xyz        50
```

### 2. Post-Reset Verify

Verifica cambios sin exponer datos:

```bash
python post_reset_verify.py
```

**Todos los valores sensibles se enmascaran automáticamente.**

---

## 📚 MEJORES PRÁCTICAS

### 1. ✅ Rotación Regular de Claves

**¿Qué es?**
Cambiar tus API keys periódicamente (cada 1-3 meses).

**Beneficios:**
- Limita el daño si una key fue comprometida
- Buena higiene de seguridad
- Cumple con mejores prácticas

**Cómo hacerlo con esta herramienta:**
```bash
# 1. Ejecutar reset
python windsurf_reset.py

# 2. Reiniciar Windsurf

# 3. Nueva API key generada automáticamente
```

### 2. ✅ Principio de Menor Privilegio

**Concepto:**
Solo dar los permisos mínimos necesarios.

**Aplicación:**
- No uses cuentas de admin si no es necesario
- Crea claves separadas para diferentes usos
- Revoca claves que ya no usas

### 3. ✅ Monitoreo de Uso

**Qué monitorear:**
- Uso inusual de API
- Peticiones desde ubicaciones extrañas
- Picos de tráfico inesperados

**Acción:**
Si detectas algo raro → **Revocar key inmediatamente**

### 4. ✅ Educación del Equipo

Si trabajas en equipo:
- Comparte esta guía
- Establece políticas claras
- Usa herramientas de gestión de secretos (Vault, AWS Secrets Manager)

---

## 🚨 QUÉ HACER SI EXPUSISTE UNA API KEY

### ⏰ Actuar RÁPIDO (minutos, no horas)

#### Paso 1: Revocar/Invalidar Inmediatamente

**Opción A: Usar esta herramienta**
```bash
# Reset completo
python windsurf_reset.py

# Reiniciar Windsurf
# Nueva key se genera automáticamente
```

**Opción B: Dashboard del servicio**
```
1. Ir a configuración de cuenta
2. Buscar "API Keys" o "Tokens"
3. Revocar/Delete la key comprometida
4. Generar nueva
```

#### Paso 2: Verificar el Daño

**Revisar logs de uso:**
- ¿Hubo peticiones no autorizadas?
- ¿Se accedió a datos sensibles?
- ¿Cuánto tiempo estuvo expuesta?

#### Paso 3: Cambiar en TODOS los Lugares

**Donde puede estar la key:**
- Variables de entorno
- Archivos `.env`
- Código fuente (si hard-coded)
- Scripts de deployment
- CI/CD pipelines
- Documentación

#### Paso 4: Actualizar Repositorios

**Si la key está en Git:**

```bash
# ⚠️ NOTA: Reescribir historia es peligroso
# Solo hazlo si entiendes las consecuencias

# Opción 1: BFG Repo-Cleaner (recomendado)
bfg --replace-text api-keys.txt my-repo.git

# Opción 2: git filter-branch
git filter-branch --tree-filter 'rm -f .env' HEAD

# Forzar push (⚠️ afecta a todos los colaboradores)
git push origin --force --all
```

**Mejor solución:**
- Considerar el repo como comprometido
- Crear nuevo repo limpio
- NO incluir historial antiguo con keys

#### Paso 5: Notificar (si aplica)

**En contexto empresarial:**
- Notificar al equipo de seguridad
- Seguir protocolo de incidentes
- Documentar lo ocurrido

**En contexto personal:**
- Cambiar otras credenciales relacionadas
- Revisar actividad de cuenta
- Habilitar 2FA si está disponible

---

## 📖 CASO DE ESTUDIO: Tu Situación

### Problema Original

Si compartes una API key públicamente:
```
sk-ws-01-********[REDACTED]
```

*(Nota: La API key real ha sido eliminada de esta documentación por seguridad)*

### Evaluación de Riesgo

**Severidad:** 🔴 ALTA

**Riesgos:**
- ✅ Key visible públicamente
- ✅ Cualquiera puede usarla
- ✅ Agota tu límite de cuenta gratuita
- ✅ Bloquea tu acceso

**Error de Windsurf:**
```
[permission_denied] free user account exceeded
```

### Solución Aplicada

1. ✅ Identificaste el problema
2. ✅ Tienes herramienta para resetear
3. ❌ **PENDIENTE:** Ejecutar reset

### Pasos Siguientes

```bash
# 1. Ejecutar reset INMEDIATAMENTE
python windsurf_reset.py

# 2. Reiniciar Windsurf

# 3. Verificar nueva key (enmascarada)
python api_key_extractor.py

# 4. NO compartir la nueva key

# 5. Documentar la lección aprendida
```

---

## 🎓 LECCIONES APRENDIDAS

### ✅ Lo Que Hacer

1. **Siempre enmascara** datos sensibles antes de compartir
2. **Usa variables de entorno** en lugar de hard-coding
3. **Rota keys regularmente** (cada 1-3 meses)
4. **Actúa rápido** si hay exposición
5. **Aprende de errores** y documenta

### ❌ Lo Que NO Hacer

1. **No hard-codear** keys en código
2. **No compartir** keys completas en chats
3. **No ignorar** advertencias de seguridad
4. **No reutilizar** keys comprometidas
5. **No postponer** el cambio de keys expuestas

---

## 🔍 VERIFICACIÓN DE SEGURIDAD

### Checklist de Auto-Evaluación

Responde honestamente:

- [ ] ¿Tienes API keys hard-coded en tu código?
- [ ] ¿Están tus keys en archivos `.env` ignorados por Git?
- [ ] ¿Rotas tus keys periódicamente?
- [ ] ¿Sabes qué hacer si expones una key?
- [ ] ¿Usas herramientas de enmascaramiento?
- [ ] ¿Tienes backups de tu configuración?
- [ ] ¿Conoces todas las ubicaciones donde están tus keys?

**Si respondiste NO a alguna:**
→ Lee las secciones relevantes de esta guía

---

## 🛠️ HERRAMIENTAS RECOMENDADAS

### Para Detección

1. **git-secrets** (GitHub)
   - Previene commits con secrets
   - Escanea repositorios existentes

2. **TruffleHog**
   - Encuentra secrets en Git history
   - Soporta múltiples tipos de credenciales

3. **detect-secrets** (Yelp)
   - Pre-commit hook
   - Plugins para diferentes tipos

### Para Gestión

1. **HashiCorp Vault**
   - Gestión centralizada de secrets
   - Rotación automática

2. **AWS Secrets Manager**
   - Para proyectos en AWS
   - Integración nativa

3. **Azure Key Vault**
   - Para proyectos en Azure
   - Cifrado de hardware

### Para Desarrollo Local

1. **python-dotenv**
   ```bash
   pip install python-dotenv
   ```

2. **direnv**
   - Auto-carga variables según directorio
   - Multiplataforma

---

## 📞 RECURSOS ADICIONALES

### Lecturas Recomendadas

1. **OWASP API Security Top 10**
   - https://owasp.org/www-project-api-security/

2. **GitHub Secret Scanning**
   - https://docs.github.com/en/code-security/secret-scanning

3. **The Twelve-Factor App**
   - https://12factor.net/config

### Comunidades

1. **r/netsec** (Reddit)
2. **Security Stack Exchange**
3. **OWASP Slack**

---

## 🎯 RESUMEN EJECUTIVO

### 3 Reglas Simples

1. **NUNCA expongas keys completas**
   - Usa enmascaramiento siempre
   - Redacta información sensible

2. **USA variables de entorno**
   - No hard-codes keys
   - Archivos `.env` en `.gitignore`

3. **ACTÚA rápido si hay exposición**
   - Revoca inmediatamente
   - Genera nueva key
   - Verifica el daño

---

## ✅ CHECKLIST FINAL

Antes de compartir CUALQUIER cosa públicamente:

- [ ] ¿Contiene API keys? → Enmascara
- [ ] ¿Contiene tokens? → Enmascara
- [ ] ¿Contiene passwords? → Elimina
- [ ] ¿Contiene URLs privadas? → Redacta
- [ ] ¿Contiene emails personales? → Considera privacidad
- [ ] ¿Es un screenshot? → Revisa TODA la pantalla
- [ ] ¿Es código? → Busca credenciales
- [ ] ¿Son logs? → Filtra información sensible

**Solo comparte cuando TODAS las respuestas sean seguras.**

---

## 🙏 CONCLUSIÓN

La seguridad NO es opcional. Es una **responsabilidad**.

**Usar esta guía te ayudará a:**
- ✅ Proteger tus credenciales
- ✅ Aprender mejores prácticas
- ✅ Evitar problemas futuros
- ✅ Ser un mejor desarrollador

**Recuerda:**
> Un minuto de prevención vale más que una hora de remediación.

---

**¡Desarrolla seguro!** 🔒

*Esta guía es parte del Windsurf Reset Tool - Proyecto Educativo*
