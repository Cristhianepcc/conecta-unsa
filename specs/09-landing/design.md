# Diseño — 09 Landing pública

## App
`core` (vistas públicas) + templates.

## Estructura (de la auditoría)
```
1. Nav     → logo · enlaces · [Iniciar sesión] · [Publicar convocatoria]
2. Hero    → titular + subtítulo + CTA primaria + secundaria + 2 puertas
3. Cómo funciona (3 pasos)
4. Convocatorias por categoría (taxonomía real, conteos reales)
5. Por qué confiar / Transparencia (semáforo)
6. Resumen semanal (teaser)
7. CTA final (egresado + empresa)
8. Footer institucional (privacidad · términos · contacto)
```

## Vistas / rutas
| Ruta | Descripción |
|---|---|
| `/` | Landing |
| `/como-funciona` `/privacidad` `/terminos` | Páginas de apoyo (placeholder con contenido base) |

## Datos (honestos)
- Conteos calculados: convocatorias activas, carreras cubiertas, índice de transparencia promedio.

## UI
- Tailwind + Alpine, branding granate (`../../branding.md`), Inter, íconos Lucide. Mobile-first, AA.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | métricas calculadas (no constantes) + test |
| CA-2 | 2 puertas en hero/nav |
| CA-3 | categorías desde taxonomía |
| CA-4 | sección transparencia con semáforo |
| CA-5 | footer + páginas privacidad/términos |
| CA-6 | revisión AA + responsive |
