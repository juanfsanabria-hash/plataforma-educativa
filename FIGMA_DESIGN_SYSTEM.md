# Sistema de Diseño - Plataforma Educativa

## 🎨 Visión

Un sistema de diseño **moderno, accesible y educativo** que:
- Se vea competitivo vs Moodle, Canvas, Google Classroom
- Sea rápido y responsivo en móvil/tablet/desktop
- Inspira confianza en instituciones educativas
- Permite UX consistente en todas las pantallas

---

## 1. Paleta de Colores

### Colores Primarios

| Uso | Hex | RGB | Tailwind |
|-----|-----|-----|----------|
| **Primario Oscuro** | `#1E40AF` | (30, 64, 175) | `blue-600` |
| **Primario** | `#2563EB` | (37, 99, 235) | `blue-600` |
| **Primario Claro** | `#3B82F6` | (59, 130, 246) | `blue-500` |
| **Primario Extra Claro** | `#93C5FD` | (147, 197, 253) | `blue-300` |

### Colores Secundarios (Complementarios)

| Uso | Hex | RGB | Tailwind |
|-----|-----|-----|----------|
| **Acento** | `#0EA5E9` | (14, 165, 233) | `cyan-500` |
| **Éxito** | `#10B981` | (16, 185, 129) | `emerald-500` |
| **Advertencia** | `#F59E0B` | (245, 158, 11) | `amber-500` |
| **Error/Crítico** | `#EF4444` | (239, 68, 68) | `red-500` |

### Escala de Grises

| Uso | Hex | Tailwind | Propósito |
|-----|-----|----------|-----------|
| **Oscuro Profundo** | `#111827` | `gray-900` | Textos principales |
| **Oscuro** | `#1F2937` | `gray-800` | Textos secundarios |
| **Gris Regular** | `#6B7280` | `gray-500` | Textos terciarios |
| **Claro** | `#F3F4F6` | `gray-100` | Fondos sutiles |
| **Blanco** | `#FFFFFF` | `white` | Fondos principales |

### Colores Pedagógicos (por rol)

| Rol | Color | Hex | Tailwind |
|-----|-------|-----|----------|
| 🎓 **Estudiante** | Azul Cielo | `#0284C7` | `sky-600` |
| 👨‍🏫 **Docente** | Verde Bosque | `#059669` | `emerald-600` |
| 👨‍👩‍👧 **Padre** | Púrpura Amable | `#7C3AED` | `violet-600` |
| 👔 **Director** | Índigo Ejecutivo | `#4F46E5` | `indigo-600` |
| ⚙️ **Admin** | Gris Profesional | `#6B7280` | `gray-600` |

---

## 2. Tipografía

### Fuentes

```css
/* Headings - Sans Serif Moderno */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;

/* Body - Sans Serif Legible */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Monospace - Código */
font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
```

### Escala Tipográfica

| Elemento | Tamaño | Weight | Line Height | Uso |
|----------|--------|--------|-------------|-----|
| **H1** | 32px / 2rem | 700 | 1.25 | Títulos de página |
| **H2** | 28px / 1.75rem | 700 | 1.3 | Subtítulos |
| **H3** | 24px / 1.5rem | 600 | 1.4 | Headers de sección |
| **H4** | 20px / 1.25rem | 600 | 1.5 | Subheaders |
| **Cuerpo** | 16px / 1rem | 400 | 1.5 | Texto principal |
| **Pequeño** | 14px / 0.875rem | 400 | 1.5 | Labels, hints |
| **Extra Pequeño** | 12px / 0.75rem | 500 | 1.5 | Badges, timestamps |

### Estilos Predefinidos

```css
/* Heading Principal */
.heading-xl {
  font-size: 2rem;        /* 32px */
  font-weight: 700;
  line-height: 1.25;
  color: #111827;         /* gray-900 */
}

/* Texto de Cuerpo */
.body-base {
  font-size: 1rem;        /* 16px */
  font-weight: 400;
  line-height: 1.5;
  color: #374151;         /* gray-700 */
}

/* Pequeña Etiqueta */
.label-small {
  font-size: 0.75rem;     /* 12px */
  font-weight: 500;
  line-height: 1.5;
  color: #6B7280;         /* gray-500 */
}
```

---

## 3. Componentes Principales

### Botones

#### Estados

```
Default    → bg-blue-600, text-white, cursor-pointer
Hover      → bg-blue-700
Active     → bg-blue-800, ring-2
Disabled   → bg-gray-300, cursor-not-allowed, opacity-50
Focus      → ring-2 ring-offset-2 ring-blue-500
```

#### Variantes

| Tipo | Fondo | Borde | Texto | Uso |
|------|-------|-------|-------|-----|
| **Primary** | `blue-600` | Ninguno | Blanco | Acciones principales |
| **Secondary** | `white` | `gray-300` | `gray-900` | Acciones secundarias |
| **Tertiary** | `gray-100` | Ninguno | `gray-700` | Acciones terciarias |
| **Danger** | `red-600` | Ninguno | Blanco | Acciones destructivas |
| **Success** | `emerald-600` | Ninguno | Blanco | Confirmación |

#### Ejemplo

```html
<!-- Primary Button -->
<button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition">
  Acción Principal
</button>

<!-- Secondary Button -->
<button class="px-4 py-2 bg-white text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition">
  Acción Secundaria
</button>
```

### Formularios

#### Inputs

```html
<div>
  <label class="block text-sm font-medium text-gray-700 mb-2">
    Etiqueta
  </label>
  <input 
    type="text"
    placeholder="Placeholder"
    class="w-full px-4 py-2 border border-gray-300 rounded-lg 
           focus:outline-none focus:ring-2 focus:ring-blue-500 
           focus:border-transparent transition"
  />
  <p class="text-sm text-red-600 mt-2">Mensaje de error (si existe)</p>
</div>
```

#### Select/Dropdown

```html
<div>
  <label class="block text-sm font-medium text-gray-700 mb-2">
    Selecciona una opción
  </label>
  <select class="w-full px-4 py-2 border border-gray-300 rounded-lg 
           focus:outline-none focus:ring-2 focus:ring-blue-500 
           focus:border-transparent transition">
    <option>-- Opción 1 --</option>
    <option>Opción 2</option>
    <option>Opción 3</option>
  </select>
</div>
```

### Cards

```html
<div class="bg-white rounded-xl shadow-md border border-gray-100 p-6 hover:shadow-lg transition">
  <h3 class="text-lg font-semibold text-gray-900 mb-2">Título Card</h3>
  <p class="text-gray-600 mb-4">Contenido descriptivo del card.</p>
  <button class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm">
    Acción
  </button>
</div>
```

### Alerts/Mensajes

```html
<!-- Success -->
<div class="p-4 rounded-lg bg-emerald-100 text-emerald-800 border border-emerald-300">
  <div class="flex">
    <span class="mr-2">✓</span>
    <div>
      <strong>Éxito:</strong> La operación se completó correctamente.
    </div>
  </div>
</div>

<!-- Error -->
<div class="p-4 rounded-lg bg-red-100 text-red-800 border border-red-300">
  <div class="flex">
    <span class="mr-2">⚠</span>
    <div>
      <strong>Error:</strong> Algo salió mal. Intenta nuevamente.
    </div>
  </div>
</div>
```

---

## 4. Grid & Layout

### Breakpoints (Tailwind)

| Nombre | Ancho Mínimo | Uso |
|--------|--------------|-----|
| `sm` | 640px | Móvil grande / Tablet |
| `md` | 768px | Tablet |
| `lg` | 1024px | Desktop pequeño |
| `xl` | 1280px | Desktop |
| `2xl` | 1536px | Desktop grande |

### Grid System

```html
<!-- 1 columna móvil, 2 tablets, 3 desktops -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Sidebar + Main Content -->
<div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
  <aside class="lg:col-span-1">
    Contenido lateral
  </aside>
  <main class="lg:col-span-3">
    Contenido principal
  </main>
</div>
```

---

## 5. Espaciado

### Escala de Espaciado (Tailwind)

```
0    → 0px
1    → 0.25rem (4px)
2    → 0.5rem (8px)
3    → 0.75rem (12px)
4    → 1rem (16px)         ← Base
5    → 1.25rem (20px)
6    → 1.5rem (24px)       ← Sección interna
8    → 2rem (32px)
12   → 3rem (48px)         ← Sección externa
16   → 4rem (64px)
```

---

## 6. Sombras & Elevación

| Nivel | Shadow | Tailwind | Uso |
|-------|--------|----------|-----|
| 0 | Ninguna | `shadow-none` | Flat design |
| 1 | Ligera | `shadow-md` | Cards normales |
| 2 | Media | `shadow-lg` | Cards hover |
| 3 | Profunda | `shadow-xl` | Modals |
| 4 | Extra | `shadow-2xl` | Dropdowns |

---

## 7. Esquinas Redondeadas

| Radio | Tailwind | Uso |
|-------|----------|-----|
| 4px | `rounded` | Inputs, botones pequeños |
| 6px | `rounded-lg` | Cards, botones |
| 8px | `rounded-xl` | Cards grandes, headers |
| 12px | `rounded-2xl` | Containers principales |
| Circular | `rounded-full` | Avatares, badges |

---

## 8. Transiciones & Animaciones

### Duración Estándar

```css
transition-all duration-150     /* 150ms - hover items */
transition-all duration-200     /* 200ms - interacciones standard */
transition-all duration-300     /* 300ms - modal opens */
```

---

## 9. Accesibilidad

### Contraste Mínimo (WCAG AA)

- ✓ Azul (#2563EB) sobre blanco: Cumple (ratio 4.5:1)
- ✓ Texto oscuro sobre fondo claro: Cumple
- ✗ Gris (#6B7280) sobre blanco: NO cumple (ratio 3.3:1) - Solo para hints

### Focus States Visibles

```css
focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
```

---

## 10. Componentes por Pantalla

### Login/Register

**Colores**: Gradiente azul (blue-50 → indigo-100)
**Layout**: Centrado, card blanco
**Componentes**: Logo, formulario, botón, divider, link alternativo

### Dashboards

**Layout**: Header + Sidebar + Main grid
**Cards**: Métricas con iconos y valores
**Gráficas**: Charts para visualización de datos

### Tablas

```html
<table class="w-full">
  <thead class="bg-gray-50 border-b border-gray-200">
    <tr>
      <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">
        Columna
      </th>
    </tr>
  </thead>
  <tbody class="divide-y divide-gray-200">
    <tr class="hover:bg-gray-50 transition">
      <td class="px-6 py-3 text-sm text-gray-700">Dato</td>
    </tr>
  </tbody>
</table>
```

---

## 11. Implementación en Código

### Ejemplo Completo: Card de Estudiante

```html
<div class="bg-white rounded-xl shadow-md border border-gray-100 p-6 hover:shadow-lg transition">
  <!-- Header -->
  <div class="flex items-start gap-4 mb-4">
    <img src="avatar.jpg" alt="Juan Pérez" class="w-12 h-12 rounded-full">
    <div>
      <h3 class="font-semibold text-gray-900">Juan Pérez García</h3>
      <p class="text-sm text-gray-600">Estudiante • 9º B</p>
    </div>
  </div>

  <!-- Metrics -->
  <div class="grid grid-cols-2 gap-4 mb-6">
    <div class="bg-blue-50 rounded-lg p-3">
      <p class="text-xs text-gray-600 mb-1">GPA</p>
      <p class="text-xl font-bold text-blue-600">8.9</p>
    </div>
    <div class="bg-emerald-50 rounded-lg p-3">
      <p class="text-xs text-gray-600 mb-1">Asistencia</p>
      <p class="text-xl font-bold text-emerald-600">95%</p>
    </div>
  </div>

  <!-- Action -->
  <button class="w-full px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition">
    Ver Perfil Completo
  </button>
</div>
```

---

## 12. Creación de Archivo Figma

### Próximos Pasos

1. Crear proyecto en Figma
2. Configurar componentes reutilizables
3. Documentar cada uno
4. Compartir con equipo
5. Sincronizar cambios con código

### URL Placeholder

```
https://www.figma.com/design/XXXXX/Plataforma-Educativa
(Por crear cuando abras Figma)
```

---

## 13. Checklist de Implementación

- ✅ Colors definidos (Tailwind)
- ✅ Typography scale establecida
- ✅ Componentes HTML básicos documentados
- ✅ Espaciado consistente
- ✅ Accesibilidad WCAG AA
- ⏳ Archivo Figma (crear después)
- ⏳ Componentes reutilizables (Django templates)
- ⏳ Testing con usuarios reales

---

## 14. Referencia Rápida

**Colores principales**: `blue-600` (#2563EB), `emerald-600` (#10B981)
**Tipografía**: System fonts (San Francisco/Segoe UI)
**Espaciado base**: 16px (tailwind `p-4`)
**Border radius**: Mostly `rounded-lg` (6px)
**Sombras**: `shadow-md` para cards, `shadow-xl` para modals

---

**Versión**: 1.0  
**Última actualización**: 2026-04-30  
**Status**: 🟢 Listo para implementación
