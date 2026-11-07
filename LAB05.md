# Laboratorio 05 — Pruebas unitarias y dobles de prueba

## 1. Datos generales

| Campo | Detalle |
|---|---|
| Curso | Ingeniería de Software II |
| Proyecto | CONECTA UNSA |
| Práctica | 05 |
| Stack de pruebas | Python 3.13, Django 6.0.6, `unittest`/Django `TestCase`, `unittest.mock` |
| Base de datos local | PostgreSQL mediante Docker Compose |

## 2. Objetivo

Automatizar pruebas unitarias y de integración del proyecto CONECTA UNSA
utilizando el framework xUnit disponible en Python (`unittest`, expuesto por
Django mediante `TestCase`), dobles de prueba con `unittest.mock` y medición
de cobertura con Coverage.py.

## 3. Organización del trabajo

El trabajo se distribuyó en un tablero GitHub Projects con las columnas:

`TO-DO` → `CURRENT ITERATION` → `IN PROGRESS` → `FIX VALIDATION` → `DONE`

| Issue | Responsabilidad | Tipo |
|---|---|---|
| #1 | Pruebas de dominio — invariantes de `Empresa` | `unit test` |
| #2 | Pruebas de dominio — servicios | `unit test` |
| #3 | Refactorización y adecuación arquitectónica | `enhancement` |
| #4 | Pruebas de repositorio — infraestructura | `unit test` |
| #5 | Configuración del entorno de mocking | `enhancement` |
| #6 | Pruebas con mocking en servicios de aplicación | `unit test` |

## 4. Caso implementado: invariantes de `Empresa`

### 4.1 Código bajo prueba

La entidad [`Empresa`](apps/empresas/models.py) define:

- `ruc`: obligatorio y compuesto exactamente por 11 dígitos.
- `razon_social`: campo obligatorio.

La validación se ejecuta explícitamente con `full_clean()`, que permite
comprobar los invariantes sin depender de una vista o formulario.

### 4.2 Especificación de casos

| Caso | Entrada | Resultado esperado |
|---|---|---|
| Creación válida | RUC `20123456789`, razón social `ACME S.A.C.` | `full_clean()` no lanza excepción |
| RUC inválido | RUC de 10 dígitos | `ValidationError` |
| Razón social vacía | `razon_social=""` | `ValidationError` |

### 4.3 Implementación

Los casos están en [`apps/empresas/tests.py`](apps/empresas/tests.py), en la
suite `EmpresaInvariantesTests`. Cada prueba sigue el ciclo:

1. **Arrange:** construir una instancia `Empresa`.
2. **Act:** ejecutar `full_clean()`.
3. **Assert:** verificar aceptación o `ValidationError`.

## 5. Trabajo simulado de los Issues #2 al #6

### Issue #2 — Servicios de dominio

Se probaron las reglas de `apps.empresas.services`:

- una empresa pendiente no puede publicar;
- una empresa activa sí puede publicar;
- `empresa_de` devuelve la empresa vinculada o `None`;
- activar y rechazar persisten únicamente el campo `estado`.

### Issue #3 — Refactorización y arquitectura

Se revisó la separación existente entre `models.py`, `services.py` y los
archivos de pruebas. La lógica de negocio ya está aislada en servicios
reutilizables, por lo que no se introdujo un refactor artificial ni cambios
de producción sin necesidad funcional. Esta decisión evita modificar
comportamiento estable únicamente para producir una diferencia en el código.

### Issue #4 — Repositorio e infraestructura

Se verificaron operaciones ORM equivalentes a un repositorio:

- recuperación de una empresa por RUC;
- unicidad del RUC;
- protección de una empresa referenciada por una convocatoria.

Estos casos ejercitan la persistencia PostgreSQL usada por Django.

### Issue #5 — Configuración de mocking

El proyecto usa `unittest.mock`, incluido en la biblioteca estándar de Python;
por tanto no requiere una dependencia adicional. Los dobles se crean con
`Mock` y las interacciones se verifican con `assert_called_once_with`.

### Issue #6 — Servicios de aplicación con dobles

`EmpresaApplicationServiceTests` reemplaza la entidad colaboradora por un
`Mock` y verifica que `activar_empresa` y `rechazar_empresa` cambien el estado
y guarden únicamente ese campo. Así se prueba la coordinación del servicio sin
acceder a la base de datos.

Los casos están separados por responsabilidad:

- [`test_servicios_lab05.py`](apps/empresas/test_servicios_lab05.py)
- [`test_repositorio_lab05.py`](apps/empresas/test_repositorio_lab05.py)
- [`test_mocking_lab05.py`](apps/empresas/test_mocking_lab05.py)
- [`test_aplicacion_lab05.py`](apps/empresas/test_aplicacion_lab05.py)

## 6. Ejecución

Con Docker iniciado:

```bash
make build
make up
make migrate
make test
```

Para ejecutar únicamente la suite del Issue #1:

```bash
docker compose run --rm web pytest apps/empresas/tests.py -k invariantes
```

El resultado que debe registrarse en la entrega es la salida real del comando,
incluyendo la cantidad de pruebas aprobadas.

Resultado verificado en este repositorio:

```text
155 passed in 97.51s
TOTAL  3331  173  95%
```

La suite específica del Issue #1 contiene tres casos y cubre la aceptación de
una entidad válida y el rechazo de los dos valores inválidos definidos en la
tabla anterior.

## 7. Cobertura

Coverage.py está declarado en `requirements.txt` como dependencia del
entorno de pruebas.

```bash
docker compose run --rm web coverage run -m pytest
docker compose run --rm web coverage report
docker compose run --rm web coverage html
```

El informe HTML se genera en `htmlcov/index.html`. La entrega debe incluir el
porcentaje mostrado por `coverage report` y una captura o referencia al
reporte HTML generado.

## 8. Dobles de prueba

La parte de mocking se implementa en los Issues #5 y #6. Para Python se
utiliza `unittest.mock`, evitando acceder a la base de datos real cuando se
prueba una colaboración de servicio con un repositorio.

Ejemplo de estructura:

```python
from unittest.mock import Mock

repositorio = Mock()
repositorio.buscar.return_value = objeto_esperado
```

La prueba debe verificar tanto el resultado como la interacción esperada con
el doble (`assert_called_once_with(...)`).

## 9. Evidencia y cierre

Para cerrar el Issue #1:

1. Ejecutar la suite y conservar la salida aprobada.
2. Ejecutar la cobertura y registrar el porcentaje.
3. Revisar los cambios.
4. Crear un commit descriptivo que incluya `Fix #1`.
5. Publicar la rama `development` o la rama de trabajo definida por el equipo.
6. Mover la tarjeta por `FIX VALIDATION` y luego `DONE`.
7. Cerrar el Issue #1 cuando la revisión esté aprobada.

Ejemplo de commit:

```bash
git add apps/empresas/tests.py LAB05.md
git commit -m "test: validar invariantes de Empresa. Fix #1"
git push origin HEAD
```
