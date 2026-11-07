# Laboratorio 05 — Pruebas unitarias y dobles de prueba

## 1. Datos generales

| Campo | Detalle |
|---|---|
| Docente | D.Sc. Edgar Sarmiento Calisaya |
| Carrera | Escuela Profesional de Ciencia de la Computación |
| Curso | Ingeniería de Software II |
| Proyecto | CONECTA UNSA |
| Práctica | 05 |
| Duración | 4 horas |
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

### 3.1 Estado de tareas

| Issue | Responsable simulado | Columna final | Estado del Issue | Commit |
|---|---|---|---|---|
| #1 | Ronald Valdez Agüero | Por confirmar | Por confirmar | `8e5bea4` |
| #2 | Fernando Llosa | Por confirmar | Por confirmar | `e32adeb` |
| #3 | Christian Taipe | Por confirmar | Por confirmar | `6122b77` |
| #4 | Luis Morales | Por confirmar | Por confirmar | `f487489` |
| #5 | Roberto Enao | Por confirmar | Por confirmar | `b3fa9ee` |
| #6 | Juan Postigo | Por confirmar | Por confirmar | `29dbe0d` |

Cada commit fue realizado separadamente y contiene `Fix #<número>` para
relacionarlo con su Issue. Las columnas y estados deben confirmarse en GitHub
Projects antes de presentar el informe.

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

### 4.3 Tabla formal de prueba

| Clase/método | Caso de prueba | Valores de prueba | Resultado esperado |
|---|---|---|---|
| `Empresa.full_clean` | Aceptar entidad válida | RUC `20123456789`, razón social `ACME S.A.C.` | No lanzar excepción |
| `Empresa.full_clean` | Rechazar RUC inválido | RUC `1234567890` | Lanzar `ValidationError` |
| `Empresa.full_clean` | Rechazar razón social vacía | `razon_social=""` | Lanzar `ValidationError` |

### 4.4 Implementación

Los casos están en [`apps/empresas/tests.py`](apps/empresas/tests.py), en la
suite `EmpresaInvariantesTests`. Cada prueba sigue el ciclo:

1. **Arrange:** construir una instancia `Empresa`.
2. **Act:** ejecutar `full_clean()`.
3. **Assert:** verificar aceptación o `ValidationError`.

## 5. Tablas de casos del equipo

| Issue | Clase/método probado | Caso | Valores | Resultado |
|---|---|---|---|---|
| #1 | `Empresa.full_clean` | Validar invariantes | RUC válido, razón social válida | Aprobado |
| #2 | `empresa_puede_publicar` | Solo una empresa activa publica | `None`, pendiente, activa | Aprobado |
| #2 | `empresa_de` | Resolver empresa vinculada | Usuario con/sin reclutador | Aprobado |
| #4 | `Empresa.objects.get` | Recuperar por RUC | RUC persistido | Aprobado |
| #4 | Restricción `unique` | Rechazar RUC duplicado | Dos empresas con el mismo RUC | Aprobado |
| #4 | `on_delete=PROTECT` | Proteger empresa referenciada | Empresa con convocatoria | Aprobado |
| #5 | `Mock` | Configurar retorno y verificar llamada | `buscar_por_ruc("20123456789")` | Aprobado |
| #6 | `activar_empresa` | Coordinar activación y guardado | Doble en estado pendiente | Aprobado |
| #6 | `rechazar_empresa` | Coordinar rechazo y guardado | Doble en estado pendiente | Aprobado |

### 5.1 Ciclo TDD y refactorización

Para cada caso se aplicó el ciclo de trabajo solicitado:

1. Se definió el comportamiento esperado en la tabla de casos.
2. Se implementó la prueba automatizada.
3. Se ejecutó la prueba en el contenedor `web`.
4. Se ajustó la implementación o la prueba cuando fue necesario.
5. Se verificó el resultado verde y se separó la responsabilidad por archivo.

La evidencia final disponible es el historial de commits y las salidas de
pytest. No se conserva una captura de cada ejecución roja intermedia.

## 6. Trabajo simulado de los Issues #2 al #6

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

## 7. Ejecución

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

### 7.1 Resultados por suite

| Suite | Pruebas |
|---|---:|
| Invariantes de `Empresa` (Issue #1) | 3 aprobadas |
| Servicios de dominio (Issue #2) | 3 aprobadas |
| Repositorio/ORM (Issue #4) | 3 aprobadas |
| Configuración de mocking (Issue #5) | 1 aprobada |
| Servicios de aplicación con mocks (Issue #6) | 2 aprobadas |
| Suite completa del proyecto | 155 aprobadas |

## 8. Cobertura

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

## 9. Dobles de prueba

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

## 10. Prerrequisitos del IDE

La ejecución validada se realizó por terminal dentro de Docker. No se
instalaron extensiones de VS Code en Ubuntu para esta práctica. Las herramientas
equivalentes usadas fueron:

| Requisito de la guía | Herramienta usada | Evidencia |
|---|---|---|
| Framework xUnit | `unittest.TestCase` + `pytest` | 155 pruebas aprobadas |
| Cobertura | Coverage.py | 95% y `htmlcov/index.html` |
| Dobles de prueba | `unittest.mock` | Issues #5 y #6 |
| Entorno | Docker Compose | Servicio `web` y PostgreSQL |

Las extensiones de VS Code son opcionales para visualizar resultados; no
reemplazan la ejecución reproducible dentro del contenedor.

## 11. Evidencia y cierre

Para cerrar los Issues:

1. Ejecutar la suite y conservar la salida aprobada.
2. Ejecutar la cobertura y registrar el porcentaje.
3. Revisar los cambios.
4. Crear un commit descriptivo que incluya `Fix #<número>`.
5. Publicar la rama de trabajo definida por el equipo.
6. Mover cada tarjeta por `FIX VALIDATION` y luego `DONE`.
7. Cerrar cada Issue cuando la revisión esté aprobada.

### 11.1 Lista de material para presentar

- [ ] Enlace al repositorio y a la rama entregada.
- [ ] Captura del tablero con las seis tarjetas en `DONE`.
- [ ] Captura de `155 passed`.
- [ ] Captura de `coverage report` mostrando `95%`.
- [ ] Captura o enlace al reporte `htmlcov/index.html`.
- [ ] Este informe `LAB05.md`.
- [ ] Historial de commits `Fix #1` a `Fix #6`.

Ejemplo de commit:

```bash
git add apps/empresas/tests.py LAB05.md
git commit -m "test: validar invariantes de Empresa. Fix #1"
git push origin HEAD
```
