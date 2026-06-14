# Requisitos No Funcionales (NFR)

> Aplican a **todas** las features. Cada feature los hereda.

## Seguridad
- **NFR-SEC-1:** Si una vista requiere un rol, entonces el sistema debe denegar el acceso a roles no autorizados.
- **NFR-SEC-2:** El sistema debe almacenar todos los secretos en variables de entorno (nunca en el repo).
- **NFR-SEC-3:** Mientras `DEBUG=False`, el sistema debe forzar HTTPS, CSRF y cookies seguras.
- **NFR-SEC-4:** El rol admin se otorga **solo** por `AdminAllowlist`, nunca por elección del usuario.

## Privacidad (Ley 29733)
- **NFR-PRIV-1:** Cuando un usuario se registra, el sistema debe capturar **consentimiento informado** del tratamiento de datos.
- **NFR-PRIV-2:** Mientras la credencial pública esté activa, el sistema debe servirla con `noindex` y solo por su URL (no buscable).
- **NFR-PRIV-3:** El sistema debe permitir al egresado controlar qué credenciales son visibles y revocar su URL pública.
- **NFR-PRIV-4:** Datos verificados por sync son **solo lectura** para el egresado; solo lo autodeclarado es editable.

## Accesibilidad (WCAG 2.1 AA)
- **NFR-A11Y-1:** El sistema debe cumplir contraste AA (texto granate `#7A1F2C` sobre blanco lo cumple).
- **NFR-A11Y-2:** El sistema debe ser navegable por teclado con foco visible y "saltar al contenido".
- **NFR-A11Y-3:** El sistema debe usar HTML semántico, `alt` en imágenes y cuerpo ≥16px.

## Internacionalización / Locale
- **NFR-I18N-1:** El sistema debe operar en **español** (`es`), zona horaria **America/Lima**, moneda **PEN (S/)**.

## Performance / Operación
- **NFR-PERF-1:** El sistema debe servir páginas en server-rendered sin build de Node.
- **NFR-PERF-2:** El sistema debe funcionar con un solo servicio web + Postgres (sin Celery/Redis).
- **NFR-PERF-3:** Mientras se usen archivos de empresa, el sistema debe referenciarlos por **URL** (Railway FS efímero).

## Mantenibilidad
- **NFR-MNT-1:** Toda regla variable (taxonomía, elegibilidad, pesos, parámetros) debe ser **editable por el admin** sin desplegar código.
