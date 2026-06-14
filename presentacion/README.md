# Presentación final — CONECTA UNSA

Carpeta de materiales para la sustentación ante el jurado.

## Contenido

- [`cumplimiento-normativo.md`](cumplimiento-normativo.md) — Respuesta a los lineamientos del Estado peruano: norma → cómo se cumple → evidencia en el código. **Entregable principal.**

## Pendientes (orden recomendado para el día 3)

1. [x] Documento de cumplimiento normativo
2. [x] PWA mínima (manifest + service worker) — instalable como app móvil
3. [ ] Captura de Lighthouse (score de Accesibilidad) — requiere Chrome (pendiente)
4. [ ] Toque de lengua originaria (lema en quechua en landing) — opcional

## Cómo demostrar la PWA en el demo

1. Levantar el servidor: `.venv/bin/python manage.py runserver`
2. Abrir `http://localhost:8000` en el navegador del celular o del laptop.
3. El navegador ofrecerá **"Instalar app"** / "Agregar a pantalla de inicio".
4. Se abre en ventana propia (sin barra del navegador), con ícono UNSA.
