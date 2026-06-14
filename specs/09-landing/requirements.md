# Requisitos — 09 Landing pública

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../../landing-audit.md`](../../landing-audit.md).

## Objetivo
Página pública institucional que comunica el valor y dirige a egresados y empresas, con datos
**honestos** y estructura de la auditoría.

## Alcance
- **Incluye:** hero, 2 puertas (egresado/empresa), cómo funciona, categorías, transparencia, resumen semanal, footer institucional.
- **No incluye:** vanity metrics (eliminadas en la auditoría).

## Historias de usuario
- **HU-1:** Como visitante, quiero entender qué es y a quién sirve en segundos.
- **HU-2:** Como egresado/empresa, quiero una entrada clara a mi flujo.

## Criterios de aceptación (EARS)
- **CA-1:** El sistema **no** debe mostrar cifras infladas; toda métrica visible debe **calcularse de datos reales** sembrados.
- **CA-2:** El sistema debe ofrecer dos entradas claras: **"Soy egresado"** y **"Soy empresa"**.
- **CA-3:** El sistema debe mostrar las **categorías** desde la taxonomía real con conteos reales.
- **CA-4:** El sistema debe explicar la transparencia con el semáforo 🟢🟡🔴.
- **CA-5:** El sistema debe incluir footer institucional con **Política de Privacidad**, Términos y contacto.
- **CA-6:** El sistema debe cumplir WCAG AA y ser responsive (NFR-A11Y).

## Dependencias
- `01-taxonomia`, `04-convocatorias`, `seed-demo`.

## Notas
- Reemplaza vanity stats por "Cómo funciona" / métricas honestas.
