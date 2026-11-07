# Arquitectura del módulo Empresas

## Responsabilidades

- `models.py`: entidades `Empresa` y `Reclutador`, estados e invariantes simples.
- `services.py`: reglas de dominio y casos de uso reutilizables.
- `forms.py`: validación y adaptación de entrada HTTP.
- `views.py`: coordinación de solicitudes y respuestas, sin duplicar reglas de dominio.
- `tests.py`: pruebas de flujos HTTP y reglas existentes de la feature.
- `test_servicios_lab05.py`: pruebas unitarias aisladas de servicios para el Issue #2.

## Regla de dependencias

Las vistas pueden usar servicios y modelos. Las pruebas de servicios no necesitan
crear una base de datos cuando validan reglas puras; utilizan objetos simples
para representar sus colaboradores. Las operaciones que verifican persistencia
se mantienen como pruebas Django separadas.

## Decisión para el Issue #3

No se introdujo una capa de repositorio artificial sobre Django ORM. El ORM ya
es la abstracción de persistencia del proyecto y las consultas de negocio están
encapsuladas en servicios. Mantener esta decisión evita duplicar código y
conserva el monolito modular definido en [`arquitectura.md`](../../arquitectura.md).
