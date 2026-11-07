# Configuración de mocking

El proyecto utiliza `unittest.mock`, que forma parte de la biblioteca estándar
de Python 3.13. No se agrega una dependencia externa para crear dobles.

## Convención

```python
from unittest.mock import Mock

repositorio = Mock()
repositorio.buscar_por_ruc.return_value = empresa
resultado = repositorio.buscar_por_ruc(ruc)
repositorio.buscar_por_ruc.assert_called_once_with(ruc)
```

El doble sustituye únicamente la colaboración externa. La prueba conserva la
lógica del servicio bajo prueba y verifica el resultado y la interacción.

La configuración se verifica en
[`test_mocking_lab05.py`](test_mocking_lab05.py). Las pruebas de comportamiento
del servicio con este doble corresponden al Issue #6.
