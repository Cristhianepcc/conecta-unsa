# Laboratorio 06 — Pruebas funcionales

## 1. Datos generales

| Campo | Detalle |
|---|---|
| Docente | D.Sc. Edgar Sarmiento Calisaya |
| Carrera | Escuela Profesional de Ciencia de la Computación |
| Curso | Ingeniería de Software II |
| Laboratorio | 06 |
| Duración | 2 horas |
| Proyecto | CONECTA UNSA |
| Tecnología | Python 3.13, Django 6.0.6 y Docker |
| Herramienta funcional | Selenium Python 4.26.0 |
| Framework de ejecución | pytest + Django `StaticLiveServerTestCase` |

## 2. Adaptación de la guía

La guía presenta un proyecto Java 17 con Maven, Spring Boot, JUnit y Selenium
Java. CONECTA UNSA utiliza Python y Django, por lo que la adaptación es:

| Guía original | CONECTA UNSA |
|---|---|
| Java 17 | Python 3.13 |
| Maven | Docker Compose + Makefile |
| Spring Boot | Django |
| JUnit/xUnit | `unittest.TestCase` + pytest |
| Selenium Java | Selenium Python |
| `localhost:8083` | servidor live de Django |
| Create Product | Registro de empresa y acceso a convocatorias |

## 3. Objetivo

Automatizar flujos funcionales de caja negra mediante un navegador real,
verificando que las acciones visibles del usuario produzcan los resultados
esperados en CONECTA UNSA.

## 4. Distribución simulada del equipo

| Issue | Integrante | Contribución | Commit |
|---|---|---|---|
| #7 | Cristhianepcc | Selenium, Chromium y Chromedriver en Docker | `7974952` |
| #8 | JPostigo48 | Base Selenium con `setUpClass` y `tearDownClass` | `1079d38` |
| #9 | rcenaov | Flujo funcional de registro de empresa | `33f839a` |
| #10 | luissfernando | Flujo funcional de acceso a convocatorias | `9109d40` |
| #11 | Fllosam | Comandos de ejecución y reporte JUnit XML | `a108285` |
| Informe | chriistmas | Consolidación de `LAB06.md` | Pendiente |

Los commits se realizaron separadamente y usan `Fix #<número>` para asociar
cada contribución con su Issue correspondiente.

## 5. Configuración

Selenium y Chromium se instalan en la imagen `web` mediante
[`Dockerfile`](Dockerfile) y [`requirements.txt`](requirements.txt).
El navegador se ejecuta en modo headless, sin interfaz gráfica:

```python
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
```

La configuración reutilizable está en
[`functional_tests/test_selenium_base.py`](functional_tests/test_selenium_base.py).

## 6. Casos de prueba de caja negra

| Objeto/funcionalidad | Escenario y acciones | Valores de prueba | Resultado esperado |
|---|---|---|---|
| Página principal | Abrir `/` con Selenium | URL del live server | El título y contenido muestran `CONECTA UNSA` |
| Registro de empresa | Abrir registro, completar campos y enviar | RUC `20123456789`, datos válidos | Redirección a `/empresas/registro/exito/` y mensaje `¡Registro enviado!` |
| Registro de empresa | Completar y enviar RUC inválido | RUC `1234567890` | El formulario permanece y muestra el error de 11 dígitos |
| Publicar convocatoria | Abrir `/empresas/publicar/` sin sesión | Usuario anónimo | Redirección al login |
| Publicar convocatoria | Iniciar sesión como reclutador y abrir la ruta | Empresa activa y reclutador válido | Se muestra el formulario `Publicar convocatoria` |

Los casos aplican una estrategia de caja negra basada en clases de equivalencia:
datos válidos, RUC inválido, usuario anónimo y usuario autenticado con rol
reclutador.

## 7. Implementación

Las pruebas están separadas del código de producción:

- [`functional_tests/test_selenium_base.py`](functional_tests/test_selenium_base.py):
  navegador, servidor live y prueba de la página principal.
- [`functional_tests/test_registro_empresa.py`](functional_tests/test_registro_empresa.py):
  registro válido y RUC inválido.
- [`functional_tests/test_convocatoria_acceso.py`](functional_tests/test_convocatoria_acceso.py):
  autorización y acceso al formulario de convocatorias.

Cada caso contiene una acción de usuario y una aserción sobre URL, título o
contenido visible. El navegador se cierra en `tearDownClass`.

## 8. Ejecución

Construir la imagen y ejecutar la suite funcional:

```bash
make build
make functional-test
```

Generar el reporte JUnit XML:

```bash
make functional-report
```

Resultado verificado:

```text
5 passed, 3 warnings
```

El reporte se genera en `tmp/lab06-junit.xml`. El directorio `tmp/` está
ignorado por Git porque contiene artefactos de ejecución.

## 9. Evidencias

- [ ] Captura del navegador o del resultado funcional.
- [ ] Captura de `make functional-test` con `5 passed`.
- [ ] Reporte `tmp/lab06-junit.xml`.
- [ ] Captura del tablero con las tareas en `DONE`.
- [ ] Historial de commits `Fix #7` a `Fix #11`.
- [ ] Este informe `LAB06.md`.

## 10. Conclusión

La suite funcional verifica desde Chromium real los flujos públicos y
protegidos más relevantes del módulo Empresas. La ejecución es reproducible
dentro de Docker y no depende de Java, Maven ni de una instalación local del
navegador.
