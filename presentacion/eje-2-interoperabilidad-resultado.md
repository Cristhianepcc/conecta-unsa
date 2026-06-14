# Eje 2 — Interoperabilidad e integración · Resultado

**Estado:** ✅ Implementado y verificado · Fecha: 2026-06-14

## Qué pedía el eje (textual)
> *Inputs y Status Indicators:* campos de entrada (*Inputs*) donde, al ingresar un DNI,
> la plataforma muestre un indicador de "Validación" en tiempo real que indique que los
> datos provienen de la base de datos académica de la UNSA.
> *Placeholders:* textos guía sobre qué información institucional se está jalando
> automáticamente, reforzando la transparencia de la integración.

Idea de fondo: la plataforma debe **conectarse** con sistemas existentes, no reemplazarlos.

## Cobertura de los 3 requisitos
| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Input de DNI | ✅ | `completar_perfil.html` — `input name="dni"` |
| 2 | Status indicator en tiempo real (datos de la UNSA) | ✅ | Iconos ⏳/✅/⚠️ + "Validando con la base académica de la UNSA…" / "✅ Validado con la UNSA · nombre · carrera" |
| 3 | Placeholders sobre qué info institucional se jala | ✅ | Placeholder del DNI + textos guía permanentes bajo carrera y estado académico |

## Dónde aparece (no es el login)
El login no cambia (cuenta institucional/Google). El DNI se valida en la pantalla
**"Completa tu perfil"**, que sale solo en el **primer ingreso** del egresado:
1. Inicia sesión (sin DNI).
2. Primer ingreso → "Completa tu perfil" → aquí valida el DNI.
3. Validado → entra a su panel (ya no vuelve a ver esa pantalla).

## Qué dato escribe el usuario vs. qué trae el sistema
- **Escribe:** solo el DNI.
- **Trae automáticamente de la UNSA:** nombres, carrera, estado académico y la fuente ("UNSA").
- Si el DNI valida, carrera y estado se autocompletan y quedan en **solo lectura**.
- Si el DNI no está en el padrón, el egresado puede **autodeclarar** sus datos (no bloquea).

## Qué se construyó
- **App nueva `apps/integraciones/`** (frontera de integración con contrato estable):
  - `padron.py` — `consultar_dni(dni)` resuelve contra `PADRON_DEMO`; en producción se
    reemplaza el cuerpo por la llamada al servicio institucional (PIDE) sin tocar vistas ni UI.
  - `views.py` + `urls.py` — endpoint `GET /api/validar-dni/` con `@login_required`.
- **Modelo:** `PerfilTalento` gana `identidad_verificada` y `dni` (migración `0003`).
- **Formulario:** `CompletarPerfilForm` añade `dni`; carrera/estado pasan a opcionales.
- **Vista `completar_perfil`:** el **servidor revalida** el DNI (no confía en el cliente);
  DNI válido → datos verificados del padrón; si no → autodeclaración obligatoria.
- **UI `completar_perfil.html`:** input de DNI con indicador en vivo, autocompletado y
  bloqueo de selects, y textos guía permanentes.
- **Seed:** la egresada demo queda con `dni=12345678`, `identidad_verificada=True`.

## Privacidad (Ley 29733)
- El DNI **nunca** se muestra en la credencial pública ni en datos visibles para empresas
  (verificado por búsqueda en plantillas).
- La validación crítica vive en el servidor; el bloqueo de campos en la UI es solo usabilidad.

## Verificación
- `python manage.py check` → sin problemas; migración `0003` aplicada.
- Endpoint: anónimo → 302 (login requerido); DNI válido → JSON correcto; no encontrado;
  formato inválido → 400 con mensaje.
- Flujo POST: DNI válido (verificado), sin datos (bloquea con error), autodeclarado (ok).
- Tests: `apps/integraciones/tests.py` (7) + suite `apps/usuarios` → **31 tests OK**.

## Cómo probarlo en navegador
1. `python manage.py runserver`
2. Entrar como egresado y llegar a `/usuarios/completar-perfil/`.
3. DNIs de demo: `12345678`, `87654321`, `44556677` (válidos); cualquier otro → autodeclarado.
