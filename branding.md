# Sistema de Diseño — CONECTA UNSA

> Norte: **estilo gobierno digital / innovación pública** (`paginas.md`), siguiendo los
> referentes **gob.pe**, **U.S. Web Design System (USWDS)** y **GOV.UK**:
> paleta sobria, mucho espacio en blanco, tipografía legible, alto contraste, componentes consistentes.
> Objetivo: transmitir **confianza institucional**.

---

## 1. Color (tokens)

El granate es el primario; se acompaña de grises y colores semánticos (para el semáforo de
transparencia y los estados de validación).

| Token | Hex | Uso |
|---|---|---|
| **granate-700 (marca)** | `#7A1F2C` | Header, botones primarios, títulos |
| granate-800 | `#52151E` | Hover |
| granate-900 | `#3D1016` | Footer |
| granate-100 | `#F5DEE1` | Badges, fondos suaves |
| granate-50 | `#FBF2F3` | Fondos muy suaves |
| neutral 50→900 | grises fríos (slate) | Texto, bordes, fondos |
| **success** | `#2E7D5B` | Alta transparencia 🟢 / Validada |
| **warning** | `#B7791F` | Media 🟡 / Incompleta |
| **danger** | `#C0392B` | Baja 🔴 / Rechazada / Duplicado |
| **info** | `#2563EB` | Avisos neutros |
| acento dorado (opcional) | `#C8A02C` | Detalles pequeños, con mesura |

**Accesibilidad:** `#7A1F2C` sobre blanco ≈ contraste 9:1 → **WCAG AA y AAA** para texto.
No usar granate claro como color de texto principal (contraste insuficiente).
Inclusión = parte del discurso del proyecto (Ley 29973).

---

## 2. Logo

- **Escudo UNSA:** usar el **archivo oficial tal cual** (idealmente SVG). **No** redibujarlo ni alterarlo.
- **"CONECTA UNSA":** wordmark/lockup → `[escudo] | CONECTA UNSA`, "CONECTA" en peso medio,
  "UNSA" en granate. No es un logotipo nuevo; es un sub-brand tipográfico (como en los mockups).
- **Provisional:** lockup tipográfico + placeholder del escudo, reemplazable sin retrabajo
  (el logo va como componente único).

### Pendiente
- [ ] Archivo del **escudo UNSA oficial** (PNG alta resolución o SVG).

---

## 3. Tipografía

- **Familia única: Inter** (Google Fonts, variable) — para títulos y cuerpo.
- Alternativa "estética gobierno": **Public Sans** (tipografía open-source del USWDS para
  interfaces de gobierno). Cambiar es trivial si se prioriza esa narrativa.
- **Escala:** 12 / 14 / 16 / 20 / 24 / 32 / 40 px.

---

## 4. Sistema visual

| Aspecto | Decisión |
|---|---|
| Espaciado | Grilla de **8px**, mucho aire ("espacios amplios") |
| Radio de bordes | 8–12px (institucional) |
| Sombras | Sutiles, elevación baja |
| Íconos | **Lucide** (un solo set, open source) |

---

## 5. Resumen

| Decisión | Valor |
|---|---|
| Primario | Granate `#7A1F2C` + escala |
| Semánticos | success/warning/danger/info |
| Acento | Dorado `#C8A02C` (opcional, mesurado) |
| Tipografía | **Inter** |
| Logo | Escudo UNSA oficial + wordmark "CONECTA UNSA" (placeholder provisional) |
| Sistema | Grilla 8px · radio 8–12px · sombras sutiles · íconos Lucide |
