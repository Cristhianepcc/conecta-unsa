# Diseño — 15 Empleabilidad

## App
`empleabilidad` (nueva, un solo dueño) · reusa `notificaciones` y `taxonomia`

## Modelo (sync gate en modelo-datos.md)
```
Evento
  titulo            CharField
  descripcion       TextField
  tipo              CharField  (taller | charla | feria | mentoria)
  fecha             DateTimeField
  modalidad         CharField  (presencial | remoto | hibrido)
  ubicacion         CharField  (blank)
  enlace_inscripcion URLField  (externo; la plataforma no inscribe)
  carreras_objetivo M2M(Carrera, blank)   # vacío = abierto a todas
  creado_en         DateTimeField

  @property futuro  → fecha >= ahora
```

## Servicios
```
# apps/empleabilidad/services.py
eventos_para(usuario)   → Evento.futuros() filtrados por carrera del perfil (o sin objetivo)
publicar_evento(evento) → notifica in-app SOLO a egresados de carreras_objetivo
                          (PerfilTalento.filter(carrera__in=...) → notificar(...TIPO_GENERAL))
```
- La difusión segmentada **no** crea infraestructura: reusa `notificaciones.notificar`.
- `mensaje_institucional` actual queda como "a todos"; este añade la variante segmentada.

## Integración
- Admin: alta de `Evento` vía Django admin (MVP) o panel (`12`).
- Egresado: nueva sección/ruta `empleabilidad/` (o pestaña en dashboard) que lista
  `eventos_para(request.user)`. Reusa la tarjeta y estilos existentes.

## UI
- Tarjeta de evento (fecha, modalidad, carreras, botón "Inscribirme" → enlace externo).
- Entrada desde el dashboard del egresado y desde la campana cuando llega el aviso.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | modelo `Evento` + admin |
| CA-2,4 | `eventos_para` (futuros + carrera) + test |
| CA-3 | `publicar_evento` → `notificar` segmentado + test |
| CA-5 | campo `enlace_inscripcion` (externo) |

## Riesgos / decisiones
- Mantener inscripción **externa** evita convertir el canal en gestor de eventos (coherente
  con el alcance acotado de `propuesta.md`).
- Es la feature de mayor esfuerzo de las tres; parte ~50% hecha (difusión + tipos
  `taller`/`evento` ya en `PerfilTalento`).
