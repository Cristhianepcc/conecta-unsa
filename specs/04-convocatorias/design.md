# Diseño — 04 Convocatorias

## App
`convocatorias`

## Modelos
```
Convocatoria
  ├─ empresa : FK → Empresa
  ├─ creada_por : enum(empresa, admin)
  ├─ tipo : enum(8)
  ├─ # Nivel 1: titulo, descripcion, modalidad, ubicacion, duracion_estimada,
  │            fecha_limite, medio_postulacion, email_contacto, no_discriminacion(bool)
  ├─ # Nivel 2 (nullable, según tipo): subvencion_remuneracion, jornada_horas, requiere_convenio,
  │            ciclo_minimo, tiempo_egreso, regimen, bases_url, cronograma, entidad_otorgante, no_vinculo
  ├─ # Nivel 3 (nullable): banda_salarial_min/max, salario_confidencial, vacantes, beneficios, discapacidad
  ├─ carreras_objetivo : M2M → Carrera
  ├─ estado : enum(borrador, pendiente, publicada, observada, rechazada, caducada)
  └─ transparencia_pct : Int (calculado)
```

## Servicios
- `campos_requeridos(tipo)` → qué Nivel 2 exige cada tipo (tabla de `modelo-datos.md` §2).
- `validar_legal(conv)` → subvención ≥ RMV, jornada ≤ tope, voluntariado sin pago (CA-4,5).
- `calcular_transparencia(conv)` → suma `PesoTransparencia` presentes → % y etiqueta (CA-6,7).

## Formulario dinámico (UI)
- 3 bloques (Alpine `x-show` según `tipo`): Esencial / Según tipo / Mejora (opcional).
- Barra de transparencia en vivo. Guardar borrador / Publicar.

## Configuración
- RMV y topes desde `ParametroLegal`; pesos desde `PesoTransparencia` (config-as-data).

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1,3 | enum tipo + `campos_requeridos` + form Alpine |
| CA-4,5 | `validar_legal` + test |
| CA-6,7 | `calcular_transparencia` + test |
| CA-8 | M2M + `taxonomia.expandir` |
| CA-9 | `creada_por` + empresa referencial |
| CA-10 | validación checkbox al publicar |
