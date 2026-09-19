# Práctica 03 — Construcción automática

| **DOCENTE** | **CARRERA** | **CURSO** |
|---|---|---|
| DSc. Edgar Sarmiento Calisaya | Ciencia de la Computación | Ingeniería de Software II |
| **PRÁCTICA** | **TEMA** | **DURACIÓN** |
| 03 | Construcción automática | 4 horas |

## 1. Proyecto seleccionado

Para esta práctica se utilizó **CONECTA UNSA**, una aplicación web institucional desarrollada con **Django**, **Python**, **HTML**, **JavaScript** y **PostgreSQL**.

- **Repositorio:** `Cristhianepcc/conecta-unsa`
- **Rama de trabajo:** `practice_03/automated_construction`
- **Tipo de aplicación:** aplicación web monolítica
- **Estado del proyecto:** proyecto avanzado en desarrollo; no es necesario que todas sus funcionalidades estén terminadas para demostrar la construcción automática.

El propósito de la práctica es demostrar que el proyecto puede configurarse, construirse, ejecutarse y probarse de forma reproducible.

## 2. Competencias relacionadas

La práctica permite aplicar herramientas de ingeniería de software para:

- Automatizar la construcción de un proyecto.
- Gestionar dependencias.
- Configurar un entorno reproducible.
- Ejecutar migraciones y pruebas automatizadas.
- Documentar el proceso de construcción.
- Utilizar Git, ramas y commits para controlar los cambios.

## 3. Objetivo

Construir y ejecutar el proyecto CONECTA UNSA mediante un modelo de construcción automática que permita:

- Definir el entorno de ejecución.
- Declarar e instalar las dependencias.
- Levantar PostgreSQL automáticamente.
- Ejecutar las migraciones de Django.
- Validar la configuración del proyecto.
- Ejecutar las pruebas automatizadas.
- Iniciar y detener la aplicación mediante comandos reproducibles.

## 4. Entorno utilizado

| Elemento | Versión o descripción |
|---|---|
| Sistema operativo | Ubuntu 24.04.5 LTS x86_64 |
| Python instalado localmente | 3.12.3 |
| Docker Engine | 29.8.0, build 88096ef |
| Docker Compose | v5.5.1 |
| Python utilizado por la aplicación | 3.13, mediante `python:3.13-slim` |
| Framework | Django 6.0.6 |
| Base de datos | PostgreSQL 16 |
| Pruebas | pytest 9.1.0 y pytest-django 4.12.0 |
| Control de versiones | Git y GitHub |

Aunque Ubuntu tiene Python 3.12.3 instalado, el servicio web se ejecuta dentro de un contenedor basado en `python:3.13-slim`. Por ello, las dependencias de Python no necesitan instalarse directamente en el sistema operativo.

## 5. Herramienta de construcción automática

Se utilizó **Docker y Docker Compose** como herramienta de construcción, aislamiento y orquestación.

Docker permite construir una imagen reproducible para Django y ejecutar PostgreSQL en un contenedor independiente. De esta manera, el entorno de desarrollo no depende de las versiones de Python, Django o PostgreSQL instaladas directamente en Ubuntu.

### 5.1 Archivos que forman el modelo de construcción

| Archivo | Responsabilidad |
|---|---|
| `Dockerfile` | Define la imagen del servicio Django, la versión de Python y la instalación de dependencias. |
| `docker-compose.yml` | Coordina los servicios `web` y `db`, puertos, volúmenes y healthcheck. |
| `requirements.txt` | Declara las bibliotecas Python y sus versiones. |
| `.dockerignore` | Evita copiar archivos innecesarios o sensibles a la imagen. |
| `Makefile` | Simplifica y automatiza los comandos de construcción, ejecución, pruebas y limpieza. |
| `manage.py` | Ejecuta tareas administrativas de Django. |
| `pytest.ini` | Configura pytest para trabajar con Django. |

## 6. Comparación con un proyecto Java y Maven

| Elemento | En un proyecto Java | En el proyecto Django |
|---|---|---|
| Archivo de construcción | `pom.xml` | `Dockerfile` y `docker-compose.yml` |
| Gestión de dependencias | Maven | `requirements.txt` y `pip` dentro del contenedor |
| Compilador | `javac` | No existe una compilación tradicional equivalente; Python es interpretado |
| Versión del lenguaje | JDK configurado en Maven | Python 3.13 definido por `FROM python:3.13-slim` |
| Base de datos | Configurada por el proyecto | Servicio PostgreSQL 16 en Docker |
| Construcción | `mvn install` | `docker compose build` o `make build` |
| Pruebas | `mvn test` | `pytest` o `make test` |
| Migraciones | Herramienta adicional | `python manage.py migrate` o `make migrate` |
| Ejecución | `java -jar` | `docker compose up` o `make up` |
| Empaquetado | `.jar` o `.war` | Imagen Docker reproducible |

Python no requiere compilación como Java. Sin embargo, Docker automatiza la preparación del entorno, la instalación de dependencias, la configuración de servicios y la ejecución de la aplicación.

## 7. Actividades

### 7.1 Configuración de la herramienta de construcción

Se verificó la instalación de Docker y Docker Compose en Ubuntu mediante:

```bash
docker --version
docker compose version
```

Resultados obtenidos:

```text
Docker version 29.8.0, build 88096ef
Docker Compose version v5.5.1
```

También se verificó la configuración del proyecto:

```bash
docker compose config
```

La configuración fue aceptada correctamente.

El archivo `docker-compose.yml` define:

- El servicio `db`, basado en `postgres:16`.
- El servicio `web`, construido desde el `Dockerfile`.
- El volumen persistente `pgdata`.
- La publicación de los puertos 5432 y 8000.
- Un healthcheck para comprobar que PostgreSQL está disponible.
- La dependencia de `web` respecto a `db` mediante `condition: service_healthy`.

### 7.2 Creación del modelo de construcción

El modelo de construcción se implementó mediante `Dockerfile`, `docker-compose.yml`, `requirements.txt` y `Makefile`.

#### 7.2.1 Información del proyecto

| Propiedad | Valor |
|---|---|
| Nombre | CONECTA UNSA |
| Repositorio | `Cristhianepcc/conecta-unsa` |
| Rama | `practice_03/automated_construction` |
| Tipo | Aplicación web Django |
| Lenguaje principal | Python |
| Versión de Python del contenedor | 3.13 |
| Base de datos | PostgreSQL 16 |
| Puerto web | 8000 |
| Puerto de PostgreSQL | 5432 |

#### 7.2.2 Opciones de construcción

El `Dockerfile` contiene:

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

El proceso de construcción realiza las siguientes acciones:

1. Utiliza una imagen base con Python 3.13.
2. Define `/app` como directorio de trabajo.
3. Copia `requirements.txt` antes del código fuente.
4. Instala las dependencias con `pip` dentro de la imagen.
5. Copia el código del proyecto.
6. Expone el puerto 8000.
7. Inicia Django con el servidor de desarrollo.

#### 7.2.3 Gestión de dependencias

Las dependencias se encuentran en `requirements.txt` y se instalan automáticamente durante la construcción de la imagen.

Principales dependencias:

| Dependencia | Función |
|---|---|
| Django 6.0.6 | Framework web principal |
| gunicorn 26.0.0 | Servidor WSGI para producción |
| psycopg | Conexión con PostgreSQL |
| dj-database-url | Configuración de la base de datos mediante URL |
| whitenoise | Servicio de archivos estáticos |
| Pillow | Procesamiento de imágenes |
| django-allauth | Autenticación y cuentas sociales |
| resend | Envío de correo |
| python-dotenv | Lectura de variables de entorno |
| segno | Generación de códigos QR |
| pytest | Ejecución de pruebas |
| pytest-django | Integración entre pytest y Django |

#### 7.2.4 Automatización mediante Makefile

El `Makefile` ofrece una interfaz simplificada para ejecutar las tareas frecuentes:

| Comando | Función |
|---|---|
| `make help` | Muestra los comandos disponibles |
| `make build` | Construye las imágenes Docker |
| `make up` | Inicia los servicios en segundo plano |
| `make stop` | Detiene los servicios sin eliminarlos |
| `make down` | Detiene y elimina contenedores y redes |
| `make restart` | Reinicia los servicios |
| `make migrate` | Ejecuta las migraciones |
| `make check` | Verifica la configuración de Django |
| `make test` | Ejecuta las pruebas automatizadas |
| `make collectstatic` | Recopila archivos estáticos |
| `make logs` | Muestra los logs |
| `make clean` | Elimina contenedores y redes huérfanas |
| `make reset` | Elimina contenedores, redes y volumen de PostgreSQL |

> `make reset` elimina los datos de la base de datos. Debe utilizarse solo cuando se desea reiniciar completamente el entorno.

### 7.3 Construcción del proyecto

La imagen se construyó con:

```bash
docker compose build
```

También puede ejecutarse mediante:

```bash
make build
```

Durante este proceso Docker:

1. Descargó la imagen `python:3.13-slim`.
2. Copió `requirements.txt`.
3. Instaló las dependencias dentro de la imagen.
4. Copió el código fuente.
5. Generó la imagen `conecta-unsa-web`.

No fue necesario instalar Django, pytest ni PostgreSQL directamente en Ubuntu.

### 7.4 Inicialización de los servicios

Los servicios se iniciaron con:

```bash
docker compose up -d
```

O mediante:

```bash
make up
```

Se verificó el estado con:

```bash
docker compose ps
```

Resultado obtenido:

```text
NAME                 IMAGE              SERVICE   STATUS                    PORTS
conecta-unsa-db-1    postgres:16        db        Up (healthy)               0.0.0.0:5432->5432/tcp
conecta-unsa-web-1   conecta-unsa-web   web       Up                        0.0.0.0:8000->8000/tcp
```

El servicio PostgreSQL se encontraba saludable y Django estaba disponible en:

```text
http://localhost:8000
```

### 7.5 Ejecución de migraciones

Las migraciones se ejecutaron dentro del contenedor mediante:

```bash
docker compose run --rm web python manage.py migrate
```

También pueden ejecutarse con:

```bash
make migrate
```

Las migraciones crean las tablas necesarias para que Django trabaje con PostgreSQL.

### 7.6 Verificación de configuración

Se puede comprobar la configuración del proyecto con:

```bash
docker compose run --rm web python manage.py check
```

O mediante:

```bash
make check
```

Este comando permite encontrar errores de configuración antes de utilizar la aplicación.

### 7.7 Ejecución de pruebas automatizadas

Las pruebas se ejecutaron dentro del contenedor mediante:

```bash
docker compose run --rm web pytest
```

También pueden ejecutarse mediante:

```bash
make test
```

Resultado obtenido:

```text
143 passed, 59 warnings in 76.69s
```

Las 143 pruebas finalizaron correctamente. Las advertencias indicaron inicialmente que no existía el directorio `staticfiles/`; no provocaron fallos en las pruebas.

Para generar los archivos estáticos se utiliza:

```bash
make collectstatic
```

### 7.8 Detención y liberación de recursos

Para detener los servicios conservando los contenedores:

```bash
make stop
```

Para detener y eliminar los contenedores y la red:

```bash
make down
```

Para eliminar también los volúmenes y reiniciar la base de datos desde cero:

```bash
make reset
```

Para consultar los logs:

```bash
make logs
```

## 8. Resultados de construcción

La construcción automática fue exitosa porque se verificó que:

- Docker Compose aceptó la configuración.
- La imagen del servicio web se construyó correctamente.
- Python 3.13 se ejecutó dentro del contenedor.
- Las dependencias se instalaron dentro de Docker.
- PostgreSQL 16 inició correctamente.
- El healthcheck de PostgreSQL fue satisfactorio.
- Django pudo conectarse a la base de datos.
- Las migraciones se ejecutaron correctamente.
- La aplicación estuvo disponible en el puerto 8000.
- Las 143 pruebas automatizadas pasaron correctamente.

## 9. Flujo completo reproducible

El flujo principal para construir, iniciar, validar y probar el proyecto es:

```bash
make build
make up
make migrate
make check
make test
```

Para detener el entorno:

```bash
make down
```

Para consultar las opciones disponibles:

```bash
make help
```

## 10. Entregables

### 10.1 Proyecto GitHub

El proyecto se encuentra en el repositorio:

```text
Cristhianepcc/conecta-unsa
```

La práctica se desarrolló en la rama:

```text
practice_03/automated_construction
```

Los cambios principales fueron:

- Incorporación de `Dockerfile`.
- Incorporación de `.dockerignore`.
- Incorporación de `Makefile`.
- Documentación de la práctica en `Pr_3_Automatic_Build.md`.
- Uso de commits para registrar los cambios.

### 10.2 Modelo de construcción

El modelo de construcción está compuesto por:

- `Dockerfile`.
- `docker-compose.yml`.
- `requirements.txt`.
- `.dockerignore`.
- `Makefile`.

### 10.3 Tutorial de instalación y construcción

#### Requisitos

- Ubuntu o cualquier sistema compatible con Docker.
- Git.
- Docker Engine.
- Docker Compose.

No es necesario instalar Django, PostgreSQL ni las bibliotecas Python directamente en el sistema operativo cuando se utiliza Docker.

#### Clonar el repositorio

```bash
git clone https://github.com/Cristhianepcc/conecta-unsa.git
cd conecta-unsa
git checkout practice_03/automated_construction
```

#### Construir el proyecto

```bash
make build
```

#### Iniciar los servicios

```bash
make up
```

#### Ejecutar migraciones

```bash
make migrate
```

#### Validar Django

```bash
make check
```

#### Ejecutar pruebas

```bash
make test
```

#### Abrir la aplicación

Ingresar en el navegador a:

```text
http://localhost:8000
```

#### Detener los servicios

```bash
make down
```

## 11. Conclusiones

1. Es factible aplicar construcción automática sobre un proyecto Django avanzado sin que todas sus funcionalidades estén terminadas.
2. Docker permite reproducir el entorno de Python y PostgreSQL sin instalar las dependencias directamente en Ubuntu.
3. `Dockerfile`, `docker-compose.yml` y `requirements.txt` cumplen funciones equivalentes a la definición de construcción y dependencias en un proyecto Java con Maven.
4. El `Makefile` simplifica la construcción, inicialización, validación, pruebas y liberación de recursos.
5. La ejecución de 143 pruebas exitosas demuestra que el entorno construido es funcional.
6. El uso de una rama independiente permite conservar el historial de cambios y separar el trabajo de la práctica del resto del desarrollo.
7. El modelo implementado es reproducible: otra persona puede clonar el repositorio y ejecutar los mismos comandos para obtener un entorno equivalente.

## 12. Evidencias recomendadas

Para la presentación o entrega se pueden adjuntar capturas de:

1. La rama `practice_03/automated_construction` en GitHub.
2. La salida de `docker compose config`.
3. La salida de `make build`.
4. La salida de `docker compose ps`, mostrando PostgreSQL saludable y Django activo.
5. La aplicación funcionando en `http://localhost:8000`.
6. La salida de `make check`.
7. La salida de `make test`, mostrando `143 passed`.
8. El historial de commits de la rama.
