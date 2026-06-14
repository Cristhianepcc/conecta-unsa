# Requisitos — 03 Empresas

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../../auth-roles.md`](../../auth-roles.md) §4-7.

## Objetivo
Permitir el auto-registro de empresas (estilo UNI, por RUC) con activación manual, y soportar
empresas "referenciales" creadas por el admin.

## Alcance
- **Incluye:** Empresa (RUC), Reclutador (1), registro, estados (pendiente/activa/rechazada), empresa referencial, badge verificada.
- **No incluye:** crear convocatorias (en `04`), dashboard empresa (en `11`).

## Historias de usuario
- **HU-1:** Como empresa, quiero registrarme por mi RUC y datos, para poder publicar convocatorias.
- **HU-2:** Como administrativo, quiero activar/rechazar empresas, para controlar quién publica.
- **HU-3:** Como administrativo, quiero crear empresas "referenciales" sin cuenta, para cargar convocatorias que llegan por correo.

## Criterios de aceptación (EARS)
- **CA-1:** Cuando una empresa envía el registro (RUC + datos + reclutador), el sistema debe crearla en estado **pendiente**.
- **CA-2:** Mientras una empresa esté **pendiente**, el sistema debe impedirle publicar convocatorias.
- **CA-3:** Cuando el admin activa una empresa, el sistema debe permitirle publicar y mostrar el badge **"Verificada"**.
- **CA-4:** Cuando el admin crea una empresa **referencial** (sin reclutador), el sistema debe permitir asociarle convocatorias **sin** badge de verificada.
- **CA-5:** El sistema debe permitir **un (1)** reclutador por empresa (MVP).
- **CA-6:** El sistema debe guardar logo y banner como **URL** (no archivo).
- **CA-7:** Si el RUC ya existe, entonces el sistema debe impedir un registro duplicado.

## Dependencias
- `02-autenticacion` (login empresa), `00` (core).

## Notas legales / no funcionales
- Correo corporativo **opcional**. NFR-PERF-3 (archivos por URL).
