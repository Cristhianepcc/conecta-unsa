# Requisitos — 07 Perfil y Credencial

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../../perfil-preferencias.md`](../../perfil-preferencias.md), [`../../matching.md`](../../matching.md).

## Objetivo
Gestionar el perfil de talento del egresado (estado, carrera, credenciales de doble origen),
sus preferencias, y la credencial verificable opt-in con URL compartible.

## Alcance
- **Incluye:** perfil, credenciales (verificado/autodeclarado), preferencias, credencial pública opt-in.
- **No incluye:** el algoritmo de matching (`05`), el sync institucional real (futuro).

## Historias de usuario
- **HU-1:** Como egresado, quiero completar mi carrera, estado y credenciales para recibir mejores recomendaciones.
- **HU-2:** Como egresado, quiero ajustar preferencias (carreras extra, silenciar, frecuencia).
- **HU-3:** Como egresado, quiero activar una carta de presentación con URL para compartir.

## Criterios de aceptación (EARS)
- **CA-1:** Cuando un usuario ingresa por primera vez, el sistema debe pedirle completar carrera y estado académico.
- **CA-2:** El sistema debe permitir agregar credenciales **autodeclaradas** (editables).
- **CA-3:** Mientras una credencial sea de **fuente verificada** (sync), el sistema debe mostrarla solo lectura con badge 🟢.
- **CA-4:** El sistema debe permitir preferencias: carreras extra, silenciar categorías/tipos, tipos preferidos, frecuencia (semanal por defecto).
- **CA-5:** Cuando el egresado **activa** su credencial pública, el sistema debe generar una URL `/credencial/<slug>`.
- **CA-6:** Mientras la credencial pública esté activa, el sistema debe servirla **solo lectura**, con `noindex`, sin features sociales.
- **CA-7:** El sistema debe permitir **revocar** la URL y elegir qué credenciales son visibles (Ley 29733).

## Dependencias
- `01-taxonomia`, `02-autenticacion`, `00`.

## Notas legales
- Ley 29733 (consentimiento, control, revocación). En demo, todo autodeclarado (no hay sync).
