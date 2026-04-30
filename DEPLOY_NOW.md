# 🚀 DEPLOY AHORA - Paso a Paso (10 minutos)

## ⚠️ REQUISITOS PREVIOS

✅ Tienes cuenta en GitHub? **SÍ/NO**
✅ Tienes cuenta en Railway? **NO - Vamos a crearla**

---

## PASO 1: Crear Repo en GitHub (2 min)

### Opción A: Ya tienes repo en GitHub

```bash
# Solo salta al PASO 3
```

### Opción B: Crear nuevo repo (RECOMENDADO PARA TI)

**En GitHub:**

1. Ve a https://github.com/new
2. Nombre: `plataforma-educativa`
3. Descripción: `Plataforma moderna de gestión integral para instituciones educativas`
4. Privacidad: **Público** (para que Railway pueda acceder)
5. Click "Create repository"

**Copiar la URL que aparece** (ejemplo):
```
https://github.com/tu-usuario/plataforma-educativa.git
```

---

## PASO 2: Conectar GitHub Local (1 min)

```bash
# En tu terminal, en la carpeta del proyecto:
git remote add origin https://github.com/tu-usuario/plataforma-educativa.git
git branch -M main
git push -u origin main
```

**Verifica que funcionó:**
```bash
git remote -v
# Debe mostrar:
# origin  https://github.com/tu-usuario/plataforma-educativa.git (fetch)
# origin  https://github.com/tu-usuario/plataforma-educativa.git (push)
```

---

## PASO 3: Crear Cuenta en Railway (2 min)

**En tu navegador:**

1. Ve a https://railway.app
2. Click "GitHub" (botón de login)
3. Autoriza Railway a acceder a GitHub
4. **LISTO** - Estás dentro

---

## PASO 4: Crear Proyecto en Railway (2 min)

**En Dashboard de Railway:**

1. Click "New Project" (botón verde)
2. Selecciona "Deploy from GitHub repo"
3. Busca y selecciona: `plataforma-educativa`
4. Click "Deploy"

**Railway estará:**
- Detectando `Procfile`
- Instalando dependencias
- Buildando la app

⏳ Espera 2-3 minutos...

---

## PASO 5: Agregar PostgreSQL (1 min)

**Mientras Railway está buildeando:**

1. En tu proyecto Railway → "+ Add Service"
2. Selecciona "PostgreSQL"
3. Click "Create"

**Railway automáticamente:**
- Crea la BD
- Genera `DATABASE_URL`
- La inyecta como variable de entorno

---

## PASO 6: Configurar Variables de Entorno (3 min)

**En Railway Dashboard:**

Click en tu proyecto → "Variables"

**AGREGAR ESTAS VARIABLES:**

```env
DEBUG=False
SECRET_KEY=generarAhora()
ALLOWED_HOSTS=<tu-app>.up.railway.app
```

### 🔑 Generar SECRET_KEY

Abre una terminal Python:
```bash
python
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
# Copiar el resultado y pegarlo como SECRET_KEY en Railway
```

O más fácil - copia este template y reemplaza:
```
django-insecure-l8k#n!@p$q%^&*()_+=-qwertyuiopasdfghjklzxcvbnm1234567890
```

---

## PASO 7: Validar Deploy ✅

**En Railway:**

1. Ve a "Deployments" tab
2. Deberías ver un deployment **verde** ✓
3. Si es rojo ✗, lee los logs y revisa variables

**Ver URL en vivo:**

```
https://<tu-proyecto>.up.railway.app
```

Debería mostrar tu plataforma 🎉

---

## PASO 8: Probar Login/Register (1 min)

**En tu navegador:**

```
https://<tu-proyecto>.up.railway.app/register/
```

1. Crear cuenta de prueba:
   - Nombre: Test
   - Apellido: User
   - Email: test@example.com
   - Cédula: 1234567890 (opcional)
   - Rol: Estudiante
   - Password: TestPassword123!

2. Click "Crear Cuenta"

3. Ir a `/login/`

4. Inicia sesión con test@example.com + TestPassword123!

5. ¡Deberías ver el dashboard de estudiante! 🎓

---

## 🎯 VERIFICACIÓN FINAL

### ✅ Checklist

- [ ] Repo en GitHub
- [ ] Proyecto Railway creado
- [ ] PostgreSQL agregada
- [ ] Variables de entorno configuradas
- [ ] Deployment en verde ✓
- [ ] URL accesible en navegador
- [ ] Login/Register funciona
- [ ] Dashboard carga correctamente

---

## ⚠️ TROUBLESHOOTING

### Error: `DisallowedHost`

**Problema**: ALLOWED_HOSTS no está correcto

**Solución**:
```
Railway → Variables
ALLOWED_HOSTS=tu-app-name.up.railway.app
(sin https://, sin www)
```

### Error: `could not connect to database`

**Problema**: PostgreSQL no está conectada

**Solución**:
```
Railway → Verifica que PostgreSQL esté verde ✓
Si no, vuelve a agregar PostgreSQL service
```

### Error: `Static files not loading` (CSS/JS)

**Solución automática**: El Procfile ejecuta `collectstatic`

Si no funciona:
```
Railway → Logs → busca "collect"
Si no ves nada, redeploy manualmente
```

### App se reinicia continuamente

**Causa**: Memory, timeout, o variable faltante

**Solución**:
```
1. Railway → Logs
2. Busca "Traceback" o "Error"
3. Lee el mensaje y ajusta variable
4. Redeploy
```

---

## 📱 PRÓXIMOS PASOS (Después del Deploy)

1. **Dominio personalizado** (opcional)
   ```
   Railroad → Settings → Domains
   Agregar tu dominio .edu.co
   ```

2. **Invita usuarios reales**
   ```
   Comparte: https://tu-app.up.railway.app/register/
   ```

3. **Monitorea logs**
   ```
   Railway → Logs (revisar diariamente)
   ```

4. **Itera basado en feedback**
   ```
   Recibe sugerencias de usuarios
   Deploy automático en cada push a master
   ```

---

## 🎬 RESUMEN RÁPIDO (Si lo olvidaste)

```
1. GitHub repo: https://github.com/new
2. Push local: git push -u origin main
3. Railway account: https://railway.app (GitHub login)
4. New Project → Deploy from GitHub
5. Add PostgreSQL
6. Set variables: DEBUG, SECRET_KEY, ALLOWED_HOSTS
7. Test: /register y /login
8. ¡Done! 🎉
```

---

## 💬 SOPORTE

Si algo falla:
1. Lee los logs en Railway
2. Verifica ALLOWED_HOSTS
3. Verifica DATABASE_URL existe
4. Redeploy
5. Si persiste, revisa DEPLOYMENT.md (sección Troubleshooting)

---

**¡YA! Tu plataforma está en vivo 🚀**

Dirección: `https://<tu-app>.up.railway.app`

Próximo: Invita usuarios, recibe feedback, itera.
