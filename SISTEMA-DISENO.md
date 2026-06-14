# Sistema de diseño — CONECTA UNSA

> Guía para **generalizar el diseño** a cualquier módulo nuevo (egresado, empresa, admin, público).
> Estética: *gobierno digital sobrio + premium* — inspiración LinkedIn, Stripe Dashboard, Notion, Linear, Coursera.
> Stack: **Django templates + Tailwind (CDN) + Alpine.js + Lucide icons**. Sin build de Node. UI en español.

Si construyes una pantalla nueva, **reutiliza lo de aquí antes de inventar**. Todo lo que se
describe ya existe en el repo.

---

## 1. Principios

1. **Datos honestos.** Ninguna cifra inflada: todo se calcula de la BD (config-as-data). No inventes métricas ni gráficos de relleno.
2. **Jerarquía clara.** Un foco principal por pantalla; lo accionable primero.
3. **Menos crómo, más aire.** Whitespace generoso, pocas líneas divisorias, sombras sutiles.
4. **Accesibilidad AA** como requisito, no como extra (foco visible, contraste, aria).
5. **Reutiliza componentes** (partials) en vez de duplicar markup.
6. **Móvil primero / responsive** siempre (sidebar off-canvas ya resuelto en el shell).

---

## 2. Tokens

### Color (definidos en `tailwind.config` dentro de `templates/base.html`)

| Token | Hex | Uso |
|---|---|---|
| `granate-700` | `#7A1F2C` | **Primario** (botones, activos, acentos) |
| `granate-800` / `900` | `#52151E` / `#3D1016` | Hovers, hero oscuro, footer |
| `granate-50` / `100` | `#FBF2F3` / `#F5DEE1` | Fondos suaves, chips, avatares |
| `exito` | `#2E7D5B` | Estados positivos / transparencia alta |
| `alerta` | `#B7791F` | Atención / transparencia media / observada |
| `peligro` | `#C0392B` | Errores / transparencia baja / vencida |
| `info` | `#2563EB` | Informativo / pendiente |
| `dorado` | `#C8A02C` | Acento puntual (badges contador) |
| Neutros | `slate-50…900` | Texto, bordes, fondos |

**Regla de uso del granate:** acentos y acciones, **no** grandes áreas de relleno (excepto el hero institucional y el footer). El resto es base neutra (blanco / `slate-50`).

### Tipografía

- Fuente **Inter** (`font-sans`, ya cargada).
- Título de página: `text-2xl sm:text-3xl font-bold tracking-tight text-slate-900`.
- Título de tarjeta/sección: `text-lg font-bold text-slate-900` (o `font-semibold`).
- Subtítulo: `text-sm text-slate-500`.
- Label de formulario: `text-sm font-semibold text-slate-600` (ver `.form-pro`).
- Cuerpo: `text-sm text-slate-600/700`.
- **Evita `text-slate-400`** para texto informativo (no cumple contraste); úsalo solo para placeholders/decoración.

### Radio, sombra, borde

- Tarjetas: `rounded-2xl`, `border border-slate-200`, `shadow-sm`, opcional `hover:shadow-md`.
- Inputs / chips: `rounded-xl` / `rounded-lg` / `rounded-full` (consistencia por familia).
- Espaciado vertical entre bloques: `space-y-6`.

### Iconos

- **Lucide** vía `data-lucide="nombre"` + clases `w-4 h-4` (o `w-5 h-5`).
- Tras render dinámico (Alpine), llamar `lucide.createIcons()` (el shell ya lo hace al cargar).
- Botón de solo ícono → **`aria-label` obligatorio**.

---

## 3. Shell de dashboard (layout de 2 zonas)

Toda vista autenticada hereda de **`templates/dashboard_base.html`** (sidebar claro + topbar; sin header/footer público).

```django
{% extends "dashboard_base.html" %}
{% load static %}

{% block title %}Mi pantalla — CONECTA UNSA{% endblock %}
{% block dashboard_title %}Título en la topbar{% endblock %}
{% block user_role %}{{ rol_o_nombre }}{% endblock %}
{% block sidebar_promo %}Frase institucional corta.{% endblock %}
{% block sidebar_items %}{% include "miapp/_sidebar_rol.html" with seccion="inicio" %}{% endblock %}
{% block topbar_actions %}<!-- CTA contextual + campana ya incluida -->{% endblock %}

{% block dashboard_content %}
<div class="max-w-screen-2xl space-y-6">
  ...
</div>
{% endblock %}
```

- Ancho de contenido: `max-w-screen-2xl` (dashboards densos) o `max-w-5xl` (formularios).
- La **campana de notificaciones** y el bloque de usuario ya vienen en la topbar.

### Sidebar por rol

Crea `miapp/_sidebar_rol.html` usando el partial de enlaces (ya trae el **indicador activo en granate**):

```django
{% include "partials/_sidebar_link.html" with url="/ruta/" icono="layout-dashboard" label="Inicio" key="inicio" seccion=seccion %}
{% include "partials/_sidebar_link.html" with url="/otra/" icono="bell" label="Notificaciones" key="notis" seccion=seccion badge=no_leidas %}
```

`seccion` se pasa desde cada plantilla; el ítem cuyo `key == seccion` se marca activo. Sidebars existentes: `usuarios/_sidebar_egresado.html`, `empresas/_sidebar_empresa.html`, `core/_sidebar_admin.html`.

---

## 4. Componentes reutilizables (partials)

| Partial | Para qué | Contexto |
|---|---|---|
| `convocatorias/_transparencia.html` | Semáforo de transparencia (única fuente de verdad) | `et` (alta/media/baja), `pct`, `variant` = `bar`\|`pill`\|`dot` |
| `empresas/_estado_badge.html` | Badge de estado de convocatoria | `estado` (slug), `label` |
| `empresas/_delta.html` | Chip de tendencia 7 días | `delta` (int o None) |
| `empresas/_fecha_limite.html` | Fecha con urgencia ("vence en N días") | `fecha`, `dias` |
| `notificaciones/_campana.html` + `_fila.html` | Campana con dropdown / fila de notificación | global (context processor) |
| `core/_dato.html`, `core/_chip_filtro.html` | Dato etiquetado / chip de filtro | varía |
| `partials/_sidebar_link.html` | Enlace de sidebar con estado activo | ver §3 |

> Estos partials ya son **accesibles** (p. ej. `_transparencia` nombra el nivel en su `aria-label`). Reúsalos en lugar de recrear badges/barras.

---

## 5. Patrones de UI (copia y adapta)

### 5.1 Header card (identidad + métricas + CTA)

Tarjeta superior con avatar/inicial (o logo), título, subtítulo, métricas y CTA destacado.

```django
<section class="rounded-2xl border border-slate-200 bg-white p-5 sm:p-6 shadow-sm">
  <div class="flex flex-col lg:flex-row lg:items-center gap-5">
    <div class="flex items-center gap-4 min-w-0">
      <span class="h-14 w-14 shrink-0 rounded-2xl bg-granate-100 text-granate-700 grid place-items-center text-xl font-bold">{{ inicial }}</span>
      <div class="min-w-0">
        <h2 class="text-xl font-bold text-slate-800 truncate">{{ titulo }}</h2>
        <p class="mt-1 text-sm text-slate-500 truncate">{{ subtitulo }}</p>
      </div>
    </div>
    <a href="#" class="lg:ml-auto inline-flex items-center gap-2 rounded-xl bg-granate-700 px-5 py-2.5 text-sm font-semibold text-white hover:bg-granate-800">
      <i data-lucide="plus" class="w-4 h-4"></i> Acción principal
    </a>
  </div>
</section>
```

### 5.2 Hero institucional (variante premium del header)

Franja granate con imagen arquitectónica (`static/img/campus.jpg`) difuminada + degradado para legibilidad. Úsalo cuando quieras dar peso de marca (ej.: dashboard de empresa).

```django
<div class="relative px-5 sm:px-6 py-5 sm:py-6 bg-granate-800">
  <img src="{% static 'img/campus.jpg' %}" alt="" aria-hidden="true" class="absolute inset-y-0 right-0 h-full w-2/3 object-cover opacity-25">
  <div class="absolute inset-0 bg-gradient-to-r from-granate-900 via-granate-800/95 to-granate-800/30"></div>
  <div class="relative ..."><!-- contenido en blanco --></div>
</div>
```

### 5.3 Métricas como tarjetas (ícono + número + contexto)

```django
<div class="rounded-xl border border-slate-200 p-4">
  <dt class="flex items-center gap-2 text-xs font-medium text-slate-500">
    <span class="grid h-7 w-7 place-items-center rounded-lg bg-granate-50 text-granate-700"><i data-lucide="eye" class="w-4 h-4"></i></span>
    Vistas
  </dt>
  <dd class="mt-2 text-2xl font-bold text-slate-800 leading-none">{{ n }}</dd>
  <dd class="mt-1.5 text-xs text-slate-500">contexto honesto</dd>
</div>
```
Para tendencia usa `_delta.html`. **No** inventes flechas si no hay base de comparación real.

### 5.4 Tabla (desktop) / tarjetas (móvil) con tabs de filtro

- Escritorio: `<table>` dentro de `hidden md:block overflow-x-auto`.
- Móvil: `<ul class="md:hidden divide-y">`.
- Filtros con Alpine: `x-data="{ filtro: 'todas' }"`, botones `role="tab"` con `:aria-selected`, filas `x-show="filtro==='todas' || filtro==='{{ slug }}'"`.
- Conteos **reales** junto a cada tab.

### 5.5 Banda de atención (lo accionable primero)

```django
<div class="rounded-2xl border border-alerta/30 bg-alerta/5 p-4 flex ... gap-3">
  <span class="grid h-9 w-9 place-items-center rounded-lg bg-alerta/15 text-alerta"><i data-lucide="alert-triangle" class="w-5 h-5"></i></span>
  <p class="text-sm text-slate-600">… <strong class="text-alerta">N</strong> por corregir …</p>
  <a class="... bg-alerta text-white ...">Acción</a>
</div>
```

### 5.6 Estado vacío

Icono en círculo `bg-granate-50`, título, frase de ayuda y CTA. Patrón usado en listas sin datos.

### 5.7 Coaching / progreso

Barra `h-1.5/2/2.5 rounded-full bg-slate-100/200` + relleno coloreado por nivel; muestra "qué falta y cuánto suma" con datos reales.

---

## 6. Formularios

### 6.1 Estilo base global: `.campo`

Fuente de verdad en `templates/base.html`. Envuelve cada campo:

```django
<div class="campo"><label for="{{ f.id_for_label }}">{{ f.label }}</label>{{ f }}{{ f.errors }}</div>
```
Da estilo accesible a `input/select/textarea`, checkbox con `accent-color` granate y foco visible. Úsalo para formularios estándar.

### 6.2 Estilo "producto moderno": `.form-pro` (escopado)

Para formularios destacados (ej. publicar/editar convocatoria): inputs con fondo `#FAFAFA`, bordes suaves, altura consistente y focus elegante, **sin alterar el `.campo` global**. Envuelve el form en `.form-pro` y reusa el bloque `<style>` de `apps/convocatorias/templates/convocatorias/_form.html`.

Estructura recomendada del formulario:

```django
<fieldset class="rounded-2xl border border-slate-200/80 bg-white p-6 sm:p-8 shadow-sm">
  <legend class="float-none w-full mb-6">
    <div class="flex items-center gap-3">
      <span class="grid h-9 w-9 place-items-center rounded-xl bg-granate-700 text-white text-sm font-bold">1</span>
      <div>
        <h2 class="text-lg font-bold text-slate-900 leading-tight">Título de sección</h2>
        <p class="text-sm text-slate-500">Descripción breve.</p>
      </div>
    </div>
  </legend>
  <div class="grid gap-x-6 gap-y-5 sm:grid-cols-2"><!-- campos --></div>
</fieldset>
```

- **Grid de 2 columnas** (`sm:grid-cols-2`); textarea / campos largos a `sm:col-span-2`.
- Checkboxes en filas `.check-row` (bordeadas, fondo suave).
- Campos dinámicos por contexto con Alpine `x-show` (+ `x-cloak`).
- Si subes archivos, el `<form>` necesita `enctype="multipart/form-data"` y la vista `request.FILES`.

### 6.3 Botones

```django
<!-- Primario -->
<button class="inline-flex items-center gap-2 rounded-xl bg-granate-700 px-9 py-3 text-sm font-semibold text-white shadow-sm hover:bg-granate-800 focus-visible:ring-2 focus-visible:ring-granate-700 focus-visible:ring-offset-2 transition">…</button>
<!-- Secundario (ghost) -->
<a class="inline-flex items-center rounded-xl px-5 py-3 text-sm font-medium text-slate-500 hover:text-slate-800 hover:bg-slate-100">Cancelar</a>
<!-- Borde (terciario) -->
<a class="rounded-lg border border-granate-700 px-4 py-2 text-sm font-medium text-granate-700 hover:bg-granate-50">…</a>
```

### 6.4 Avisos (toasts)

Los `messages` de Django ya se muestran como **toasts** fijos abajo-derecha (definido en `base.html`): borde de color por tipo, ícono, auto-cierre. No los re-implementes.

---

## 7. Accesibilidad (AA) — checklist por pantalla

- [ ] Foco visible (ya global; no lo elimines con `outline-none` sin reemplazo).
- [ ] Botones de solo ícono con `aria-label`.
- [ ] Color que comunica estado **también** en texto (nombra el nivel/estado).
- [ ] Contraste: texto informativo en `slate-500/600/700`, no `slate-400`.
- [ ] Imágenes decorativas con `alt=""` + `aria-hidden="true"`.
- [ ] Tablas con `<thead>`; listas con semántica correcta.
- [ ] `aria-current="page"` en el ítem activo del sidebar (lo hace el partial).
- [ ] Funciona con teclado y respeta `prefers-reduced-motion`.

---

## 8. Responsive

- Contenedor: `max-w-screen-2xl` (dashboards) / `max-w-5xl` (forms) / `mx-auto`.
- Grids: `grid-cols-1` → `sm:grid-cols-2` → `lg:grid-cols-3/4`.
- Tabla en desktop ↔ tarjetas en móvil (§5.4).
- El sidebar off-canvas con hamburguesa ya está resuelto en el shell.

---

## 9. Interactividad (Alpine) y datos

- Estado local de UI con `x-data` (filtros, tabs, previews, cálculos en vivo).
- Para cálculos "en vivo" basados en config (ej. transparencia), pasa los pesos con
  `{{ datos|json_script:"id" }}` y léelos en Alpine — **misma fuente que el backend**.
- Cualquier número visible debe venir de la BD / servicios, no hardcodeado.

---

## 10. Cómo aplicarlo a un módulo nuevo (receta rápida)

1. Hereda de `dashboard_base.html` y rellena los `{% block %}`.
2. Crea/incluye el sidebar del rol con `_sidebar_link.html`.
3. Abre con un **header card** (§5.1) o **hero** (§5.2) si aplica.
4. Pon el **contenido protagonista** (tabla/feed/form) y deja lo informativo en paneles laterales o secciones inferiores.
5. Reutiliza partials (§4) para badges, transparencia, fechas, notificaciones.
6. Formularios con `.campo` o `.form-pro` (§6).
7. Pasa el **checklist de accesibilidad** (§7).
8. Verifica el render real con Playwright (**desktop 1440 y móvil 390**) y corre `pytest`.

---

*Referencias vivas en el repo:* `templates/dashboard_base.html`, `templates/base.html` (tokens + `.campo` + toasts),
`apps/convocatorias/templates/convocatorias/_form.html` (`.form-pro`), `apps/usuarios/templates/usuarios/dashboard.html`
y `apps/empresas/templates/empresas/dashboard.html` (patrones), y los partials de §4.
