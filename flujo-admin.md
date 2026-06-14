# Flujo Administrativo — CONECTA UNSA

> Cómo el panel administrativo transforma la gestión manual de la Bolsa de Trabajo UNSA
> en un proceso automatizado, con **control institucional** pero **mínima carga operativa**.
> Alinea: `propuesta.md` §7 (flujo administrativo) + el mockup "Flujo empresa→validación→difusión".
>
> Objetivos que cumple el panel:
> - **Segmentación automatizada** (no más "todo a todos").
> - **Matching** vacante ↔ perfil de egresado (carrera/área).
> - **Estandarización** (obliga datos críticos: salario, requisitos).
> - **Reducción de carga operativa** (el admin deja de clasificar todo a mano).
> - **Control del ruido informativo** (filtra ofertas reales, evita reenvíos).

---

## 1. Estados de la convocatoria (ciclo de vida)

6 estados — deliberadamente pocos, para minimizar clics y carga del equipo:

| Estado | Significado | Quién lo activa |
|---|---|---|
| **Borrador** | La empresa la guardó, aún no la envió | Empresa |
| **Pendiente** | Enviada y prevalidada por el sistema; espera decisión del admin | Sistema (al publicar) |
| **Publicada** | Validada y difundida a egresados pertinentes | Admin (o auto, ver §4) |
| **Observada** | Devuelta a la empresa para corregir (recuperable) | Admin / Sistema |
| **Rechazada** | No cumple (ej. requisitos discriminatorios) — terminal | Admin |
| **Caducada** | Pasó su fecha límite | Sistema (automático) |

`Incompleta`, `Duplicada` y `Exceso de difusión` **no son estados**: son **alertas** (ver §2).

---

## 2. Alertas del sistema (prevalidación básica)

Se calculan automáticamente y se muestran **sobre las convocatorias Pendientes**, para que
el admin sepa **dónde mirar** sin clasificar todo a mano (`propuesta.md` §7 Paso 2):

| Alerta | Color | Disparador |
|---|---|---|
| Posible duplicado | 🔴 | Ver regla en §3 |
| Información incompleta | 🟡 | Faltan campos fundamentales (Nivel 1) |
| Baja transparencia | 🟡 | % de transparencia < 50% |
| Posible exceso de difusión | 🟠 | La empresa supera un límite de publicaciones en el período |

---

## 3. Detección de duplicados

Regla (sin IA — la propuesta lo prohíbe):

> **Misma empresa** (mismo RUC/email) **+ título muy parecido + dentro de los últimos 30 días.**

- "Muy parecido" se mide con **`pg_trgm`**, la extensión nativa de PostgreSQL para similitud
  de texto: normaliza el título (minúsculas, sin tildes) y calcula un **% de similitud**.
- Simple, nativo del stack y **100% auditable**: el admin ve *"85% de similitud con la convocatoria X"*.
- Si supera el umbral → alerta 🔴 **posible duplicado**. **El admin confirma**; el sistema no borra solo.
- Opcional para reducir falsos positivos: exigir además que coincidan las **carreras objetivo**.

---

## 4. ¿Aprobación humana siempre? — Semáforo de confianza (híbrido)

Reduce carga **sin** perder el control que exige una entidad pública:

| Caso | Decisión |
|---|---|
| **Empresa nueva** o convocatoria **con alertas** (baja transparencia, posible duplicado, requisitos sospechosos) | 🔴 **Revisión humana obligatoria** antes de publicar |
| **Empresa verificada/recurrente** + convocatoria **sin alertas** y **alta transparencia 🟢** | 🟢 **Auto-publicación**; el admin **audita por muestreo** después |

- La **primera vez**, una empresa **siempre** pasa por un humano (control institucional).
- Una vez que la UNSA confía en ella, sus buenas convocatorias fluyen solas → el admin deja
  de ser cuello de botella. Es la *"priorización asistida"* de `propuesta.md` §4.

---

## 5. Difusión segmentada (matching)

Una vez **Publicada**, la convocatoria se difunde **solo a los perfiles pertinentes** usando
las **carreras objetivo** (taxonomía UNSA: Área → Facultad → Carrera). Nunca a listas globales.
Es el mecanismo que reemplaza el "enviar todo a todos" y sostiene la confianza del egresado.

---

## 6. Flujo completo (resumen)

```
Empresa registra ──> [Pendiente] ──> Prevalidación automática (alertas)
                                          │
                          ┌───────────────┴────────────────┐
                  ¿empresa verificada                ¿alertas o
                   y sin alertas y 🟢?                empresa nueva?
                          │ sí                              │ sí
                   [Auto-Publicada]                  Revisión humana
                   (audita por muestreo)                    │
                                              ┌─────────────┼─────────────┐
                                         [Publicada]   [Observada]   [Rechazada]
                                              │
                                     Difusión segmentada
                                     (carreras objetivo) ──> Egresados pertinentes
                                              │
                                         [Caducada] (al vencer la fecha límite)
```
