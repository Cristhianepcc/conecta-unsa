# Imágenes del proyecto

| Archivo | Dónde se usa | Estado |
|---|---|---|
| `LOGO_UNSA.png` | header y footer (`templates/base.html`) + panel del hero (`core/home.html`) | ✅ en uso |
| `campus.jpg` | foto del hero — campus UNSA (`core/home.html`) | ✅ en uso (baja resolución; reemplazable por una mejor con el mismo nombre) |

En dev se sirven automáticamente; en producción se recogen con `collectstatic` (WhiteNoise).
Los logos de empresas se cargan por URL (`Empresa.logo_url`); si están vacíos se muestra la inicial.
