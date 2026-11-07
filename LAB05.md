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

## 5. Ejecución

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
146 passed in 97.65s
TOTAL  3273  175  95%
```

La suite específica del Issue #1 contiene tres casos y cubre la aceptación de
una entidad válida y el rechazo de los dos valores inválidos definidos en la
tabla anterior.

## 6. Cobertura

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

## 7. Dobles de prueba

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

## 8. Evidencia y cierre

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
