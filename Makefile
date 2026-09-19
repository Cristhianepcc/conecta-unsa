.PHONY: help build up stop down restart migrate check test collectstatic shell logs clean reset

COMPOSE := docker compose
WEB := $(COMPOSE) run --rm web

help:
	@echo "Comandos disponibles:"
	@echo "  make build         Construye las imagenes Docker"
	@echo "  make up            Inicia los servicios en segundo plano"
	@echo "  make stop          Detiene los servicios sin eliminarlos"
	@echo "  make down          Detiene y elimina los contenedores"
	@echo "  make restart       Reinicia los servicios"
	@echo "  make migrate       Ejecuta las migraciones de Django"
	@echo "  make check         Verifica la configuracion de Django"
	@echo "  make test          Ejecuta las pruebas automatizadas"
	@echo "  make collectstatic Recopila los archivos estaticos"
	@echo "  make shell         Abre una shell de Django"
	@echo "  make logs          Muestra los logs de los servicios"
	@echo "  make clean         Elimina contenedores y redes"
	@echo "  make reset         Elimina tambien el volumen de PostgreSQL"

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) stop

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) down
	$(COMPOSE) up -d

migrate:
	$(WEB) python manage.py migrate

check:
	$(WEB) python manage.py check

test:
	$(WEB) pytest

collectstatic:
	$(WEB) python manage.py collectstatic --noinput

shell:
	$(WEB) python manage.py shell

logs:
	$(COMPOSE) logs -f

clean:
	$(COMPOSE) down --remove-orphans

reset:
	$(COMPOSE) down --volumes --remove-orphans

