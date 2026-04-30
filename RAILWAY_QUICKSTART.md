# Railway Deployment - Guía Rápida

## 5 Pasos para Deployar en Producción

### Paso 1️⃣: Crear Cuenta en Railway (2 min)

```
1. Ve a https://railway.app
2. Click "Login" → "GitHub"
3. Autoriza Railway para acceder a tu GitHub
4. Listo
```

### Paso 2️⃣: Crear Nuevo Proyecto (1 min)

```
1. Dashboard → "New Project" (botón grande verde)
2. "Deploy from GitHub repo"
3. Selecciona: plataforma-educativa
4. Click "Deploy"
   ↳ Railway detecta automáticamente el Procfile
```

### Paso 3️⃣: Agregar Base de Datos PostgreSQL (1 min)

```
1. En tu proyecto: "+ Add Service"
2. Selecciona "PostgreSQL"
3. Railway crea la BD automáticamente
4. La variable DATABASE_URL aparece automáticamente
```

### Paso 4️⃣: Configurar Variables de Entorno (5 min)

Ve a **"Project Settings" → "Variables"** y agrega:

```env
# CRÍTICAS
DEBUG=False
SECRET_KEY=<genera-una-nueva-key>
ALLOWED_HOSTS=<tu-app>.up.railway.app

# EMAIL (opcional por ahora, usa console si no quieres)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# IA (opcional)
OPENAI_API_KEY=sk-...
CLAUDE_API_KEY=sk-...
```

#### 🔑 Generar SECRET_KEY seguro:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Paso 5️⃣: Validar Deploy Automático ✅

```
1. Cada push a "master" → deploy automático
2. Ver logs en tiempo real:
   Dashboard → "Logs"
3. Ver URL en vivo:
   Dashboard → "Deployments" → URL generada
   Ejemplo: https://plataforma-educativa-production.up.railway.app
```

---

## Variables de Entorno Explicadas

| Variable | Valor | Notas |
|----------|-------|-------|
| **DEBUG** | `False` | ⚠️ SIEMPRE False en producción |
| **SECRET_KEY** | 50+ caracteres aleatorios | 🔐 Mantén segura, no la compartas |
| **ALLOWED_HOSTS** | `.up.railway.app` | Dominio automático de Railway |
| **DATABASE_URL** | `postgres://...` | ✅ Automática (creada por Railway) |
| **EMAIL_BACKEND** | `django.core.mail.backends.console.EmailBackend` | 📧 Consola para testing |
| **SECURE_SSL_REDIRECT** | Auto (True si DEBUG=False) | 🔒 Force HTTPS |

---

## Checklist Pre-Deploy

- [ ] Git push a master completado
- [ ] Django migrations escritas (`python manage.py makemigrations`)
- [ ] Archivo `Procfile` en root ✓
- [ ] Archivo `railway.json` en root ✓
- [ ] Archivo `.env.example` actualizado ✓
- [ ] `requirements.txt` actualizado ✓
- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` cambiado (no usar default)
- [ ] PostgreSQL agregada (BD automática)
- [ ] Migrations correrán automáticamente (release phase)

---

## 🚀 Después del Primer Deploy

### Ver App en Vivo

```
URL automática: https://<tu-app>.up.railway.app
```

### Ver Logs en Tiempo Real

```bash
# Opción 1: Dashboard (fácil)
Railway Dashboard → "Logs"

# Opción 2: CLI (avanzado)
npm install -g @railway/cli
railway login
railway logs
```

### Parar/Reiniciar App

```
Dashboard → "Deployments"
Click en deployment actual → "Restart" o "Stop"
```

### Rollback a Versión Anterior

```
Dashboard → "Deployments"
Selecciona deploy anterior → "Redeploy"
```

---

## Conectar Dominio Personalizado

### Opción 1: Subdominio Free (Sin costo)

```
Ya tienes: <tu-app>.up.railway.app ✓
Perfecto para MVP
```

### Opción 2: Dominio Personalizado (tuyo)

```
1. Dashboard → "Settings" → "Domains"
2. "+ Add Custom Domain"
3. Ingresa: plataforma.edu.co (ejemplo)
4. Railway muestra registros DNS
5. Configura en tu registrador de dominios:
   CNAME: <tu-app>.up.railway.app
6. Espera 24-48 horas (propagación DNS)
```

---

## Troubleshooting Común

### ❌ Error: `ModuleNotFoundError: No module named 'django'`

**Causa**: `pip install -r requirements.txt` no corrió
**Solución**: Railway lo hace automáticamente, pero revisa:
```
Dashboard → "Logs" → busca "pip install"
Si no ves nada, redeploy manualmente
```

### ❌ Error: `could not connect to server: Connection refused`

**Causa**: PostgreSQL no está conectada
**Solución**:
```
1. Dashboard → Verifica que PostgreSQL esté en verde ✓
2. Verifica variable DATABASE_URL existe
3. Si no existe, vuelve a agregar PostgreSQL service
4. Redeploy
```

### ❌ Error: `DisallowedHost: 'mi-app.up.railway.app'`

**Causa**: ALLOWED_HOSTS no incluye tu dominio
**Solución**:
```
Settings → Variables → ALLOWED_HOSTS=mi-app.up.railway.app
(sin https://, sin www. a menos que uses www)
Redeploy
```

### ❌ Static files no se cargan (CSS/JS)

**Causa**: Whitenoise no sirvió los archivos
**Solución**:
```
# Opción 1: Automática (debería funcionar)
Procfile tiene: python manage.py collectstatic

# Opción 2: Manual
railway run python manage.py collectstatic --noinput
```

### ❌ App se reinicia en loop

**Causa**: Memory leak, timeout, o variable faltante
**Solución**:
```
1. Revisa logs: Dashboard → "Logs"
2. Busca: "Traceback", "Error", "SIGKILL"
3. Si dice "SIGKILL" = out of memory
   → Settings → aumenta RAM (de 512MB a 1GB)
4. Si dice variable missing:
   → Settings → Variables → agrega la variable
5. Redeploy
```

---

## Performance y Scaling

### Plan Actual Recomendado (MVP)

| Componente | CPU | RAM | Precio | Para |
|-----------|-----|-----|--------|------|
| Web App | 0.5 | 512 MB | $5/mes | <1000 usuarios |
| PostgreSQL | - | 1 GB | $15/mes | <10GB datos |
| **Total** | - | - | **~$20/mes** | Producción pequeña |

### Escalado Progresivo

```
Usuarios: 100-500        → Plan actual OK
Usuarios: 500-2000       → +CPU web (aumenta a 1 CPU)
Usuarios: 2000-5000      → +RAM web (aumenta a 1GB) + DB (2GB)
Usuarios: 5000+          → Habla con Railway support
```

### Monitorear Performance

```
Dashboard → "Analytics"
Busca:
- Memory usage (máx 80%)
- CPU usage (máx 60%)
- Request latency (máx 500ms)
- Error rate (máx 1%)

Si alguno se sale:
1. Revisa logs
2. Optimiza código
3. Escala infraestructura
```

---

## Comandos Railway CLI (Opcional)

```bash
# Instalar CLI
npm install -g @railway/cli

# Autenticarse
railway login

# Ver variables de entorno
railway env

# Ver logs
railway logs --follow

# Ejecutar comando en producción
railway run python manage.py migrate
railway run python manage.py shell

# Deploy manual
railway deploy

# Ver status
railway status
```

---

## Seguridad en Producción ✅

Configurado automáticamente cuando `DEBUG=False`:

```python
✓ SECURE_SSL_REDIRECT = True          # Force HTTPS
✓ SESSION_COOKIE_SECURE = True        # Cookies solo HTTPS
✓ CSRF_COOKIE_SECURE = True           # CSRF protection
✓ SECURE_HSTS_SECONDS = 31536000      # 1 año
✓ Content-Security-Policy             # XSS prevention
✓ WhiteNoise middleware               # Servir archivos estáticos
```

---

## Backups Automáticos

Railway crea backups automáticos:
```
PostgreSQL → automatic daily backups
Retenidos: últimos 7 días
Restaurar: contacta support de Railway
```

---

## Preguntas Frecuentes

**P: ¿Cuesta dinero?**
R: $5-20/mes dependiendo de uso. Pay-as-you-go, sin sorpresas.

**P: ¿Cuántos usuarios soporta?**
R: MVP actual soporta ~500 usuarios concurrentes sin problemas.

**P: ¿Cómo agrego usuarios en producción?**
R: 
- Opción 1: Ir a /admin y crear manualmente
- Opción 2: Usuarios crean cuentas en /register

**P: ¿Cómo reseteo la BD?**
R: ⚠️ Peligroso, pero es posible:
```bash
railway run python manage.py flush --noinput
```

**P: ¿Puedo conectar mi dominio .com.co?**
R: Sí, sigue la sección "Dominio Personalizado".

---

## Siguiente Paso

### Una vez que esté corriendo:

1. **Prueba el flujo completo:**
   - Ir a https://tu-app.up.railway.app/register
   - Crear cuenta de prueba
   - Iniciar sesión
   - Ver dashboards

2. **Monitorea los primeros días:**
   - Revisa logs regularmente
   - Anota cualquier error
   - Ajusta variables si es necesario

3. **Después (cuando esté estable):**
   - Invita usuarios reales
   - Recolecta feedback
   - Itera el producto

---

**Fecha**: 2026-04-30  
**Status**: ✅ Listo para producción  
**Próximo**: Deploy a Railway + Sistema Figma
