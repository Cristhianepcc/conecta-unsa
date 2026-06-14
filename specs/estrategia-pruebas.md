# Estrategia de Pruebas

> Cómo cada criterio **EARS** de `requirements.md` se convierte en una prueba. En SDD, el spec es verificable.

## Principio
Cada criterio `CA-x` → al menos **un test**. La columna "Trazabilidad" de cada `design.md`
mapea criterio → código → test. Una feature no está "Done" hasta que sus CA críticos pasan.

## Qué se prueba (prioridad MVP)
1. **Lógica de servicios (lo crítico)** — matching, transparencia, duplicados, expansión de taxonomía,
   matriz de elegibilidad. Son reglas puras → tests unitarios rápidos y de alto valor.
2. **Reglas de acceso por rol** — un rol no puede ver/hacer lo de otro (NFR-SEC-1).
3. **Integridad de datos** — `PROTECT`, estados válidos, validaciones legales (subvención ≥ RMV).
4. **Flujos clave** — registro de empresa, publicar → revisar → difundir.

## Qué NO se prueba a fondo en el MVP
- Detalles visuales de templates (se validan a ojo).
- OAuth de Google (se prueba el ruteo de rol, no el handshake de Google).

## Herramientas
- **`pytest` + `pytest-django`** (o `unittest` de Django). Base de datos de test PostgreSQL.
- Datos de prueba con `factory_boy` o fixtures mínimas.

## Convención de nombres
- `test_<feature>_<CA>__<caso>` — ej. `test_taxonomia_ca4__expandir_area_devuelve_carreras`.

## Ejemplo (de `01-taxonomia`)
| Criterio | Test |
|---|---|
| CA-1 | el seed crea 3 áreas / 16 facultades / 43 carreras |
| CA-4 | `expandir(Area Ingenierías)` devuelve sus 19 carreras |
| CA-5 | borrar Carrera referenciada lanza `ProtectedError` |
