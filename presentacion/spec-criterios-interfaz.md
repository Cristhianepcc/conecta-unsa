# Spec de cumplimiento — Criterios de interfaz (Software Público)

> **Objetivo.** Demostrar, eje por eje, cómo CONECTA UNSA cumple la rúbrica de
> *Software Público peruano* (replicabilidad, interoperabilidad, estandarización,
> automatización administrativa y protección de datos), distinguiendo lo que **ya
> está construido** de los **ajustes pendientes** para cerrar el 100%.
>
> Estado base medido sobre la rama `feat/build-conecta-unsa`. Las rutas y símbolos
> citados son reales y verificables.

## Tabla de cobertura

| Eje | Estado | Falta para 100% |
|---|---|---|
| 1. Replicabilidad / componentes reutilizables | 🟢 Cumple (~95%) | Nada bloqueante; documentar el sistema de componentes |
| 2. Interoperabilidad (validación DNI/UNSA) | 🔴 Pendiente (~40%) | Input DNI + status indicator + placeholders institucionales |
| 3. Estandarización y transparencia | 🟢 Cumple (~90%) | Botón "Enviar" `disabled` proactivo en form de empresa |
| 4. Automatización del panel admin | 🟢 Cumple (~85%) | Acciones bulk (multi-select) en la bandeja |
| 5. Protección de datos personales | 🟡 Parcial (~75%) | Modal de consentimiento + vistas ARCO |

Cada eje siguiente define: **(A) qué ya cumple**, **(B) lo que se construye**,
**(C) criterios de aceptación**, **(D) archivos a tocar**.

---

## Eje 1 — Replicabilidad y componentes reutilizables (Vibe Coding)

### A. Ya cumple
- 18 partials reutilizables con prefijo `_` (cards y sections independientes):
  `apps/convocatorias/templates/convocatorias/_tarjeta.html`,
  `_oportunidad.html`, `_transparencia.html`;
  `templates/core/_valor_granate.html`, `_chip_filtro.html`, `_dato.html`;
  `apps/empresas/templates/empresas/_estado_badge.html`;
  `apps/notificaciones/templates/notificaciones/_campana.html`, `_fila.html`;
  `templates/partials/_sidebar_por_rol.html`.
- Sistema de diseño con tokens de color y clases base (`.shell`, `.campo`) en
  `templates/base.html`; grids responsive (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`).
- Jerarquía visual con paleta de 6 roles de color + escala de grises; matching
  visualmente jerarquizado (barra de compatibilidad por encima del detalle).

### B. Qué se construye (cierre)
1. **Catálogo de componentes** (`presentacion/sistema-componentes.md`): una tabla
   `componente → props (variables de contexto) → variantes → dónde se reusa`.
   Sirve a otra entidad para "tomar" un componente sin leer todo el proyecto.
2. **Convención de reuso documentada**: cada partial declara en su primera línea,
   como comentario, qué variables de contexto espera (contrato de inclusión).

### C. Criterios de aceptación
- [ ] Existe `sistema-componentes.md` con ≥12 componentes y su contrato de uso.
- [ ] Cada partial reutilizable comienza con un comentario `{# espera: var1, var2 #}`.
- [ ] Demostrable: un componente (p. ej. `_transparencia.html`) se renderiza igual
      en tarjeta, panel admin y detalle, con solo cambiar la variante.

### D. Archivos
- Nuevo: `presentacion/sistema-componentes.md`.
- Editar (comentario de contrato): los partials listados en A.

---

## Eje 2 — Interoperabilidad e integración (PRIORIDAD ALTA)

> Es el eje más débil y el de mayor retorno en la demo. La rúbrica pide
> textualmente: input de DNI con **indicador de "Validación" en tiempo real** que
> evidencie que el dato proviene de la base académica UNSA, más **placeholders**
> que expliquen qué información institucional se "jala" automáticamente.

### A. Ya cumple (base)
- Distinción de procedencia de datos: `Credencial.fuente`
  (`FUENTE_VERIFICADO` / `FUENTE_AUTODECLARADO`) en `apps/usuarios/models.py:71-76`,
  con propiedades `verificada` y `editable` (solo lo autodeclarado se edita).
- `RUC` de empresa validado con `RegexValidator` de 11 dígitos.
- Reconocimiento explícito del punto de integración: `apps/usuarios/models.py:97-98`
  (`carrera` y `estado_academico` llegarían por sync institucional, solo lectura).

### B. Qué se construye

#### B.1 — Adaptador de "padrón académico" (mock con contrato real)
Servicio único que simula la consulta institucional y queda listo para sustituir
por la integración real (PIDE/RENIEC/SUNEDU) sin tocar las vistas.

- Nuevo módulo `apps/integraciones/padron.py`:
  ```python
  # Contrato estable: en producción, esta función llama al servicio
  # institucional autorizado (PIDE). En demo, resuelve contra datos sembrados.
  def consultar_dni(dni: str) -> ResultadoPadron | None:
      """Devuelve identidad académica verificada para un DNI, o None.

      ResultadoPadron: nombres, carrera (FK Carrera), estado_academico, fuente.
      """
  ```
- El resultado **marca `fuente=verificado`**; el formulario lo trata como
  **solo lectura** (coherente con `Credencial.editable`).

#### B.2 — Endpoint de validación en vivo
- Vista JSON `GET /api/validar-dni/?dni=NNNNNNNN` (en `apps/integraciones/views.py`),
  con throttling básico y `login_required`.
- Respuestas estandarizadas:
  - `200 {"estado":"validado","nombres":...,"carrera":...,"estado_academico":...,"fuente":"UNSA"}`
  - `200 {"estado":"no_encontrado"}`
  - `400 {"estado":"formato_invalido","mensaje":"El DNI debe tener 8 dígitos."}`

#### B.3 — Input DNI con status indicator (UI)
En `apps/usuarios/templates/usuarios/completar_perfil.html`, anteponer al form:
- Input `dni` con `placeholder="Ingresa tu DNI — validaremos tu carrera con la UNSA"`.
- Indicador de estado (Alpine, ya disponible en el proyecto):
  - ⏳ `Validando con la base académica de la UNSA…`
  - ✅ `Validado con la UNSA · {nombres} · {carrera}` (badge verde)
  - ⚠️ `No encontrado — puedes continuar autodeclarando tus datos`
- Al validar OK: `carrera` y `estado_academico` se **autocompletan y bloquean**
  (`readonly`/`disabled`), con leyenda *"Dato institucional — solo lectura"*.
- Placeholders en cada campo institucional indicando el origen del dato.

#### B.4 — Persistencia de procedencia
- Al guardar perfil validado vía DNI, registrar la fuente como verificada
  (campo nuevo en `PerfilTalento`: `identidad_verificada = BooleanField(default=False)`
  + `dni` opcional, **nunca** mostrado en credencial pública).

### C. Criterios de aceptación
- [ ] Escribir 8 dígitos dispara la consulta sin recargar (≤400 ms en demo).
- [ ] DNI presente en seed → badge ✅ con nombre + carrera provenientes del "padrón".
- [ ] Campos `carrera`/`estado_academico` quedan en solo lectura tras validar.
- [ ] DNI con formato inválido → error message explicativo, no excepción.
- [ ] DNI no encontrado → permite continuar en modo autodeclarado (no bloquea).
- [ ] El adaptador `consultar_dni` está aislado: cambiar a integración real no
      requiere tocar vistas ni templates.
- [ ] El DNI nunca aparece en `credencial_publica.html` ni en respuestas a empresas.

### D. Archivos
- Nuevos: `apps/integraciones/__init__.py`, `apps/integraciones/padron.py`,
  `apps/integraciones/views.py`, `apps/integraciones/urls.py`.
- Editar: `apps/usuarios/templates/usuarios/completar_perfil.html`,
  `apps/usuarios/forms.py` (`CompletarPerfilForm`: campo `dni`, lógica readonly),
  `apps/usuarios/views.py` (`completar_perfil`),
  `apps/usuarios/models.py` (`PerfilTalento.identidad_verificada`, `dni`),
  `config/urls.py` (incluir `integraciones.urls`),
  `apps/core/management/commands/seed_demo.py` (DNIs de demo en el padrón).
- Migración: `apps/usuarios/migrations/` (campos nuevos).

---

## Eje 3 — Estandarización y transparencia (anti-opacidad)

### A. Ya cumple
- Validación legal forzosa por niveles en `apps/convocatorias/services.py`
  (`CAMPOS_NIVEL_1`, `validar_legal`); bloquea publicación si falta declaración de
  no discriminación (Ley 26772) o si la remuneración es menor a la RMV vigente,
  con error message educativo.
- Semáforo de transparencia (8 criterios ponderados) con coaching
  ("💡 Falta: beneficios, sumaría 10%") — `desglose_transparencia`.
- Rango salarial obligatorio salvo excepción declarada (`salario_confidencial`).
- Botón "Observar" del admin **ya** está `disabled` hasta escribir comentario
  (`revisar.html`, `:disabled="!c.trim()"`).

### B. Qué se construye (cierre)
1. **Botón "Enviar a revisión" `disabled` proactivo** en el formulario de empresa
   (la rúbrica lo pide literal): deshabilitado hasta que los campos críticos
   (`titulo`, `descripcion`, `modalidad`, `ubicacion`, `fecha_limite`,
   `medio_postulacion`, `email_contacto` y la casilla de no discriminación) estén
   completos. Implementación con Alpine sobre el form existente — la validación de
   servidor (`validar_legal`) permanece como salvaguarda.
2. **Error message de transparencia salarial**: si el reclutador marca
   "salario confidencial", mostrar advertencia inline no bloqueante que eduque
   ("La banda salarial visible es lo que más sube tu transparencia y atrae más
   postulantes").

### C. Criterios de aceptación
- [ ] El botón "Enviar a revisión" está `disabled` mientras falte un campo crítico,
      con `title`/tooltip explicando qué falta.
- [ ] Marcar "confidencial" muestra el mensaje educativo (sin impedir el envío).
- [ ] La validación de servidor sigue rechazando envíos incompletos (defensa en
      profundidad), aunque la UI se manipule.

### D. Archivos
- Editar: `apps/convocatorias/templates/convocatorias/_form.html` (estado Alpine
  del botón + mensaje confidencial). Sin cambios de modelo.

---

## Eje 4 — Automatización del panel administrativo

### A. Ya cumple
- Panel `core/panel_admin.html` con métricas clicables, bandeja **FIFO**
  (`order_by("creada_en")`), chips de filtro con conteos, búsqueda por título/empresa,
  alertas (`flujo.calcular_alertas`), comparador de duplicados y aprobación inline
  por fila (`apps/core/views.py:40-179`).
- Success/error messages de Django + dropdown de notificaciones.

### B. Qué se construye (cierre)
1. **Acciones masivas (bulk)** — la rúbrica pide "validar u observar ofertas
   masivamente con un solo clic":
   - Checkbox por fila + "Seleccionar todo" en la bandeja.
   - Barra de acciones bulk: **Aprobar seleccionadas** (solo habilita filas
     `sin alertas`, para no aprobar a ciegas las riesgosas).
   - Vista `POST core/acciones-masivas/` que itera con `flujo.aprobar` dentro de
     una transacción y captura `TransicionInvalida` por ítem.
2. **Success message agregado**: "Se publicaron N convocatorias; M omitidas por
   alertas" — confirma la automatización y reduce carga cognitiva.

### C. Criterios de aceptación
- [ ] "Seleccionar todo" marca solo las filas accionables (sin alertas).
- [ ] Una sola acción publica el lote; las que fallan no rompen el resto.
- [ ] Mensaje de resultado indica cuántas se publicaron y cuántas se omitieron y por qué.
- [ ] Se respeta el flujo de estados (no se salta `validar_legal`/`calcular_transparencia`).

### D. Archivos
- Editar: `apps/core/templates/core/panel_admin.html` (checkboxes + barra bulk),
  `apps/core/views.py` (nueva vista `acciones_masivas`),
  `apps/core/urls.py` (ruta).

---

## Eje 5 — Protección de datos personales

### A. Ya cumple
- `ConsentimientoForm` (Ley 29733) y registro de fecha en
  `Perfil.consentimiento_datos` / `consentimiento_en` (`apps/usuarios/models.py:36-37`).
- Credencial pública **opt-in** y `noindex` (`credencial_publica` fija
  `X-Robots-Tag: noindex, nofollow`).
- Páginas `core/privacidad.html` y `core/terminos.html`; documento
  `presentacion/cumplimiento-normativo.md`.
- Granularidad: `Credencial.visible_para_empresas` (default `False`).

### B. Qué se construye (cierre)
1. **Modal de consentimiento** (la rúbrica lo pide como *Modal*): ventana emergente
   en el primer ingreso que explica el uso de datos para el matching, antes de
   entrar a la plataforma. Reusar el patrón Alpine del dropdown de campana.
   - Checkboxes diferenciados: (a) tratamiento de datos (Ley 29733, obligatorio),
     (b) uso de carrera/credenciales para matching (obligatorio para el feed),
     (c) visibilidad de credencial pública (opcional).
   - No continúa hasta marcar los obligatorios; registra `consentimiento_en`.
2. **Vistas ARCO** (Acceso, Rectificación, Cancelación/eliminación):
   - "Descargar mis datos" (export JSON del perfil + credenciales).
   - "Eliminar mi cuenta y datos" (con confirmación), respetando que las
     credenciales verificadas provienen del padrón (se desvinculan, no se alteran
     en origen).
   - Ya existe rectificación parcial (preferencias/credenciales autodeclaradas en
     `perfil`); documentarla como parte de ARCO.

### C. Criterios de aceptación
- [ ] En el primer ingreso aparece el modal; no se accede al dashboard sin aceptar
      los consentimientos obligatorios.
- [ ] El consentimiento (qué y cuándo) queda registrado y es auditable.
- [ ] El egresado puede descargar sus datos en un clic.
- [ ] El egresado puede eliminar su cuenta; las credenciales verificadas no se
      alteran en el sistema de origen.
- [ ] El DNI (Eje 2) no se expone en exports a terceros ni en credencial pública.

### D. Archivos
- Nuevo: partial `apps/usuarios/templates/usuarios/_modal_consentimiento.html`.
- Editar: `templates/base.html` o `usuarios/completar_perfil.html` (incluir modal),
  `apps/usuarios/views.py` (export + eliminación), `apps/usuarios/urls.py`.

---

## Plan de ejecución sugerido (por impacto en la demo)

1. **Eje 2 — DNI + status indicator** (mayor retorno visual; cierra el eje débil).
2. **Eje 5 — Modal de consentimiento** (rápido, reusa patrón Alpine existente).
3. **Eje 4 — Acciones bulk** (refuerza el discurso de "automatización").
4. **Eje 3 — Botón `disabled` proactivo** (ajuste cosmético sobre lógica ya sólida).
5. **Eje 1 — Catálogo de componentes** (documentación, sin código de runtime).
6. **Eje 5 — Vistas ARCO** (completa el cumplimiento Ley 29733).

## Storyboard para la presentación (sugerido por la rúbrica)

> "De una oferta opaca a una estandarizada":
> 1. Reclutador intenta publicar sin banda salarial → **botón disabled** + coaching.
> 2. Completa datos → **semáforo de transparencia** sube de 🔴 a 🟢.
> 3. Admin recibe la oferta en la **bandeja**, ve alertas, **aprueba en lote**.
> 4. Egresado valida su **DNI con la UNSA** (badge ✅), acepta el **modal de
>    consentimiento**, y recibe la oferta por **matching explicable** (% + motivos).

## Notas de alcance

- El adaptador de padrón (Eje 2) es un **mock con contrato estable**: la demo no
  integra servicios reales del Estado, pero la frontera está diseñada para
  sustituirse por PIDE sin reescribir UI ni vistas. Declarar esto en la
  presentación evita prometer interoperabilidad que no está activa.
- Toda la lógica de validación crítica permanece en el servidor
  (`validar_legal`, decoradores de rol); los `disabled` de UI son ayuda de
  usabilidad, no el control de seguridad.
