# Auditoría UI/UX de la Landing — CONECTA UNSA

> Revisión profesional del mockup `paginas/Landing-pública-institucional.png` con criterio
> de páginas institucionales / gobierno digital (gob.pe, GOV.UK, USWDS).
> Veredicto: diseño sólido, pero comete el error más grave de una página pública —
> **cifras infladas no verificables** en un producto cuya tesis es "transparencia y confianza".
> Esta auditoría es la especificación de la landing.

---

## ✅ Conservar (funciona)
- Headline claro centrado en beneficio ("Oportunidades relevantes para egresados").
- Sección de **categorías profesionales** (el core: pertinencia).
- Sección de **transparencia** (el diferenciador real).
- Teaser de **resumen semanal** (comunica el anti-saturación).
- Paleta granate + estética gov-digital.

---

## 🔴 Eliminar

1. **Vanity metrics del hero (1.246 / 24.538 / 86% / 31.762).** Lo #1.
   - Una plataforma nueva no tiene esas cifras → son inventadas.
   - Contradice la tesis del proyecto (transparencia/confianza). Si el jurado lo nota, mata la credibilidad.
   - Las páginas institucionales serias no usan vanity metrics.
2. **Barra de búsqueda del nav** si no es funcional. UI que no hace nada erosiona confianza → construir o quitar.
3. **CTAs redundantes sin jerarquía** → una sola acción primaria evidente.
4. **Categorías que no existen en la taxonomía** → todo tile mapea a `taxonomia-unsa.md`.
5. **Tarjetas decorativas flotantes** sobre el hero → ruido visual.

---

## 🟡 Mejorar

- **Reemplazar vanity stats por "Cómo funciona" (3 pasos)** o métricas **honestas y reales**
  ("23 convocatorias activas", "43 carreras cubiertas", "Índice de transparencia: X%").
- **Dos puertas de público:** agregar entrada clara para **empresas** además de egresados
  → patrón "Soy egresado / Soy empresa".
- **Jerarquía de CTA:** 1 primaria ("Ingresar con correo UNSA") + 1 secundaria ("Cómo funciona");
  en el nav, CTA de empresas ("Publicar convocatoria").
- **Explicar el % de transparencia** con el semáforo 🟢🟡🔴.
- **Reducir densidad** → más aire (gov-digital respira).

---

## ♿ Estándares institucionales que faltan (obligatorios)
- **Accesibilidad WCAG AA:** contraste, foco visible, `alt`, "saltar al contenido", cuerpo ≥16px.
- **Footer institucional funcional:** Política de Privacidad (Ley 29733), Términos,
  contacto de la Oficina de Empleabilidad, transparencia.
- **Lenguaje claro** (plain language) y **mobile-first**.

---

## 🧭 Estructura final de la landing

```
1. Nav        → logo · enlaces · [Iniciar sesión] · [Publicar convocatoria]
2. Hero       → titular + subtítulo + 1 CTA primaria + 1 secundaria
                + 2 puertas: "Soy egresado" / "Soy empresa"
3. Cómo funciona (3 pasos)         ← reemplaza las vanity stats
4. Convocatorias por categoría     ← taxonomía real, conteos reales
5. Por qué confiar / Transparencia ← con el semáforo explicado
6. Resumen semanal (teaser)
7. CTA final (egresado + empresa)
8. Footer institucional (privacidad · términos · contacto · transparencia)
```

---

## Decisión derivada (Pregunta 9 — datos de ejemplo)

- **Cifras reales calculadas** de datos de muestra sembrados. **Nada inflado.**
- Se siembran **15–25 convocatorias** realistas repartidas por carreras/tipos para que el portal
  se vea vivo y navegable. Las estadísticas se derivan de ese set (ej. "23 convocatorias activas").
- Empresas de muestra: **ver decisión en notas de seed** (ficticias genéricas vs reales de Arequipa).
