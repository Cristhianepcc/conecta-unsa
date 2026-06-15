# Requisitos — 20 Alta de convocatoria por el administrativo (recepción manual)

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../06-flujo-admin/requirements.md`](../06-flujo-admin/requirements.md), [`../04-convocatorias/requirements.md`](../04-convocatorias/requirements.md), [`../12-panel-admin/requirements.md`](../12-panel-admin/requirements.md).

## Objetivo
Cubrir [`../../propuesta.md`](../../propuesta.md) §7-Paso 1 (Recepción): que las convocatorias
puedan ingresar también por **correo institucional o contenido copiado manualmente**, dando de
alta la convocatoria **a nombre de una empresa** desde el panel admin (no solo autopublicación).

## Contexto (estado actual del código)
- El modelo ya distingue el origen: `Convocatoria.creada_por` con `CREADA_POR_ADMIN`
  (`apps/convocatorias/models.py:25`). ✅
- **PERO no hay vista para que el admin cree una convocatoria:** `core/urls.py` solo tiene
  revisar/aprobar; el alta solo ocurre por autopublicación de empresa. ❌

## Alcance
- **Incluye:** vista en el panel admin para crear una convocatoria seleccionando la empresa,
  reusando `ConvocatoriaForm`, marcándola `creada_por = admin`, y enviándola al **mismo flujo**
  (prevalidación, duplicados, estados).
- **No incluye:** parser automático de correos entrantes (el admin copia/pega el contenido en v1);
  IMAP/ingesta automática queda como evolución futura.

## Historias de usuario
- **HU-1:** Como administrativo, quiero registrar una convocatoria que llegó por correo, a nombre
  de la empresa, para difundirla por el canal.
- **HU-2:** Como universidad, quiero trazabilidad del origen (empresa vs. admin) de cada convocatoria.

## Criterios de aceptación (EARS)
- **CA-1:** Un admin debe poder crear una convocatoria seleccionando la **empresa** y completando
  el `ConvocatoriaForm`.
- **CA-2:** Cuando un admin crea una convocatoria, el sistema debe registrar `creada_por = admin`.
- **CA-3:** Una convocatoria creada por admin debe pasar por la **misma prevalidación** (faltantes
  de nivel 1, detección de duplicados) que una de empresa.
- **CA-4:** Si el rol no es admin, entonces el acceso a la vista de alta debe ser denegado (403).

## Dependencias
- `04-convocatorias` (`ConvocatoriaForm`), `06-flujo-admin` (prevalidación/duplicados),
  `03-empresas` (`Empresa`), `12-panel-admin` (panel).

## Notas legales / no funcionales aplicables
- Control de acceso por rol (NFR-SEC-1) — reusar `admin_required`.
- **Sync gate:** sin modelo nuevo (`creada_por` ya existe); sin migración.
