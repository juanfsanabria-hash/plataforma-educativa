# Railway Deployment Guide

## Plataforma Instituciones Educativas - Production Setup

Este documento describe cómo desplegar la plataforma educativa a Railway.

---

## 1. Requisitos Previos

- Cuenta activa en [Railway.app](https://railway.app)
- Repositorio GitHub con el código
- Variables de entorno configuradas

---

## 2. Configuración en Railway

### 2.1 Crear un Nuevo Proyecto

1. Inicia sesión en [Railway.app](https://railway.app)
2. Haz clic en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Autoriza Railway a acceder a tu GitHub
5. Selecciona el repositorio `plataforma-educativa`
6. Haz clic en **"Deploy"**

### 2.2 Configurar Base de Datos PostgreSQL

Railway detectará automáticamente el `Procfile` y configurará el servicio.

**Para agregar PostgreSQL:**

1. En el dashboard del proyecto, haz clic en **"+ Add Service"**
2. Selecciona **"PostgreSQL"**
3. Railway generará automáticamente las variables de entorno:
   - `DATABASE_URL` (cadena de conexión completa)

---

## 3. Variables de Entorno

Configura las siguientes variables en Railway (**Project Settings → Variables**):

### Variables Críticas para Producción

```env
# Django
DEBUG=False
SECRET_KEY=<generate-a-secure-key-here>
ALLOWED_HOSTS=<tu-dominio>.up.railway.app,www.<tu-dominio>.com

# Database (Railway crea esto automáticamente)
# DATABASE_URL=postgres://user:password@host:port/dbname

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=<tu-email@gmail.com>
EMAIL_HOST_PASSWORD=<app-password-de-gmail>
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@plataforma-educativa.com

# IA & APIs
OPENAI_API_KEY=<tu-openai-key>
CLAUDE_API_KEY=<tu-claude-key>

# AWS S3 (Opcional, para media/static files)
AWS_ACCESS_KEY_ID=<tu-aws-key>
AWS_SECRET_ACCESS_KEY=<tu-aws-secret>
AWS_STORAGE_BUCKET_NAME=<nombre-bucket>
AWS_S3_REGION_NAME=us-east-1

# URLs de Aplicación
SITE_URL=https://<tu-dominio>.up.railway.app
SITE_NAME=Plataforma Educativa
```

### Generar SECRET_KEY Seguro

En tu máquina local, ejecuta:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y pégalo en la variable `SECRET_KEY`.

---

## 4. Configuración del Proyecto en config/settings.py

Railway proporciona la variable de entorno `DATABASE_URL`. Nuestra configuración debe leerla:

```python
import dj_database_url
import os

# Railway proporciona esta variable automáticamente
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME', 'institucion_educativa'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

# Seguridad en Producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Whitenoise para servir archivos estáticos
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 5. Dependencias Requeridas

Asegúrate de que `requirements.txt` incluya:

```
dj-database-url==2.1.0  # Para parsear DATABASE_URL
whitenoise==6.6.0       # Para servir archivos estáticos
gunicorn==21.2.0        # Servidor WSGI
```

✅ **Ya están incluidas en el proyecto**

---

## 6. El Archivo Procfile

El `Procfile` define cómo Railway ejecuta tu aplicación:

```
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 4
release: python manage.py migrate --noinput
```

- **web**: Comando principal para servir la app
- **release**: Se ejecuta antes del deploy para aplicar migraciones

---

## 7. Dockerfile (Alternativa)

Railway también puede usar el `Dockerfile` incluido en el proyecto. La configuración actual soporta ambas:

- **Opción 1**: Usar `Procfile` (Buildpack de Heroku)
- **Opción 2**: Usar `Dockerfile` (Construcción de contenedor)

Para usar Docker, Railway lo detectará automáticamente si no encuentra Procfile, o puedes configurarlo explícitamente en `railway.json`.

---

## 8. Dominio Personalizado

Una vez que tu app esté corriendo en Railway:

1. Dirígete a **Project Settings → Domains**
2. Railway asignará automáticamente un dominio `.up.railway.app`
3. Para usar tu dominio personalizado (ej: `plataforma.edu.co`):
   - Añade el dominio en **Project Settings**
   - Railway mostrará los registros DNS a configurar
   - Actualiza los DNS en tu registrador de dominios
   - Espera 24-48 horas para propagación

### Ejemplo de Registros DNS

```
CNAME: <app-name>.up.railway.app
A Record: 188.x.x.x (IP de Railway)
```

---

## 9. Despliegue Automático (CI/CD)

Railway se integra automáticamente con GitHub:

1. Cualquier push a `master` dispara un nuevo deploy
2. El `Procfile` ejecuta migraciones automáticamente
3. Los logs están disponibles en el dashboard de Railway

Para ver los logs en tiempo real:

```bash
# Instala Railway CLI (opcional)
npm i -g @railway/cli

# Login
railway login

# Ver logs
railway logs
```

---

## 10. Monitoreo y Logs

### Acceder a Logs en Railway

1. Dashboard → Tu Proyecto → Deployment
2. Haz clic en **"View Logs"**
3. Verás logs de:
   - Construcción (build)
   - Inicio (startup)
   - Ejecución (runtime)

### Alertas Recomendadas

Configura notificaciones para:
- Deploy failures
- Memory/CPU overload
- Restart loops

En **Project Settings → Notifications**

---

## 11. Escalado y Performance

### Plan Inicial (Recomendado para MVP)

- **Instancia Web**: 512 MB RAM, 0.5 CPU → $5/mes
- **PostgreSQL**: 1 GB → $15/mes
- **Total**: ~$20/mes

Para escalar:
1. Ve a **Project Settings → Plan**
2. Aumenta RAM/CPU según demanda
3. Costo aumenta proporcionalmente

### Monitoreo de Performance

Revisa el dashboard para:
- CPU usage (máx ~80%)
- Memory usage (máx ~80%)
- Request latency
- Error rates

Si alguno excede 80%, es tiempo de escalar.

---

## 12. Rollback a Versión Anterior

Si un deploy falla:

1. Railway guarda automáticamente los últimos 5 deploys
2. En el dashboard, haz clic en **"Deployments"**
3. Selecciona un deploy anterior
4. Haz clic en **"Redeploy"**

---

## 13. Variables de Entorno por Ambiente

### Desarrollo (Local)

```env
DEBUG=True
DATABASE_URL=postgres://localhost/institucion_educativa
```

### Producción (Railway)

```env
DEBUG=False
ALLOWED_HOSTS=<dominio>.up.railway.app
SECURE_SSL_REDIRECT=True
```

Railway automáticamente inyecta `DATABASE_URL` desde PostgreSQL.

---

## 14. Troubleshooting

### Error: `ModuleNotFoundError: No module named 'django'`

**Solución**: Asegúrate de que Railway ejecute `pip install -r requirements.txt` antes de `gunicorn`. El Procfile lo hace automáticamente.

### Error: `django.db.utils.OperationalError: could not connect to server`

**Solución**: Verifica que `DATABASE_URL` esté configurada. Railway debería inyectarla automáticamente al agregar PostgreSQL.

```bash
# En Railway CLI, verifica variables
railway env
```

### Error: Static files no se cargan (404)

**Solución**: Ejecuta en Railway CLI:

```bash
railway run python manage.py collectstatic --noinput
```

O permite que el `release` phase en el Procfile lo haga automáticamente.

### App se reinicia continuamente

**Solución**: Revisa los logs. Puede ser:
- Memory leak (aumenta RAM)
- Database connection timeout (revisa DATABASE_URL)
- Missing environment variable (verifica config)

---

## 15. Checklist Previo al Lanzamiento

- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` generado y no commiteado
- [ ] PostgreSQL agregada y DATABASE_URL inyectada
- [ ] Email configurado (SMTP credentials)
- [ ] S3 configurado (si usas media files)
- [ ] `python manage.py collectstatic` ejecutado
- [ ] Migrations aplicadas automáticamente
- [ ] HTTPS habilitado (SECURE_SSL_REDIRECT=True)
- [ ] ALLOWED_HOSTS incluye tu dominio
- [ ] Logs monitoreados
- [ ] Backups de base de datos configurados (Railway lo hace automáticamente)

---

## 16. Acceso a Base de Datos en Producción

### Desde Django Shell

```bash
railway run python manage.py shell
```

### Desde psql (Cliente PostgreSQL)

Obtén la URL de conexión de Railway y ejecuta:

```bash
psql "postgres://user:password@host:5432/railway"
```

---

## 17. Referencia Rápida - Comandos Railway CLI

```bash
# Instalar CLI
npm i -g @railway/cli

# Login
railway login

# Ver variables de entorno
railway env

# Ejecutar comando en producción
railway run python manage.py migrate

# Ver logs
railway logs

# Deploy manual
railway deploy

# Listar proyectos
railway list
```

---

## 📚 Recursos Adicionales

- [Railway Documentation](https://docs.railway.app)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Environment Variables Best Practices](https://12factor.net/config)

---

**Fecha de Actualización**: 2026-04-30  
**Versión de Django**: 5.0.0  
**Servidor Web**: Gunicorn 21.2.0  
**Base de Datos**: PostgreSQL (Railway)
