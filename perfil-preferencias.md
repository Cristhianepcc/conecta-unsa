# Perfil, Preferencias y Credencial — CONECTA UNSA

> Cierra la **Brecha D**. Cubre: editabilidad del perfil (dos orígenes), preferencias del
> estudiante/egresado y la **credencial verificable** (URL compartible opt-in).

---

## 1. Editabilidad del perfil (dos orígenes)

El perfil mantiene el modelo de **doble origen** (el diferenciador de confianza):

| Origen | Producción | Demo | Editable |
|---|---|---|---|
| 🟢 **Verificado (sync institucional)** | Lo trae la UNSA por sync autorizado (`propuesta.md` §6.1) | **Simulado** (no hay sync) | **No** (solo lectura) |
| ⚪ **Autodeclarado** | El estudiante lo agrega | El que ingresa lo completa/edita | **Sí** |

- **En la demo no existe el sync** → el perfil es **editable** y **autodeclarado**: cada usuario
  entra con su **propio Gmail** y completa su carrera/estado/credenciales al ingresar.
- No se siembran perfiles; el presentador usa **2–3 cuentas Gmail propias** para mostrar
  el matching en distintos estados (ver `matching.md` → Estrategia de DEMO).
- **UI:** campos verificados con badge 🟢 y solo lectura; autodeclarados editables.
- **TODO producción (comentar en código):** estado académico, carrera y credenciales
  institucionales llegan por **sync autorizado** y **no** son editables; solo lo autodeclarado se edita.
- **Registro en demo:** como no hay sync, el usuario **elige su carrera y estado académico**
  (autodeclarado). En producción vendría pre-llenado y bloqueado.

---

## 2. Preferencias del estudiante/egresado (Brecha D)

El feed ya viene armado por los filtros de `matching.md` (estado + carrera). Las preferencias
solo **afinan** — todo funciona **sin** configurar nada (mínima fricción):

| Preferencia | Qué hace | Estado |
|---|---|---|
| Carrera propia | Se sigue automáticamente | Fijo (no se quita) |
| Carreras/áreas extra de interés | Ver también convocatorias de otras carreras afines | ✅ Incluir |
| Silenciar categorías/tipos | Apagar lo que no interesa (ej. "no quiero voluntariados") | ✅ Incluir |
| Tipos de convocatoria preferidos | Ej. "solo prácticas y trainee" | ✅ Incluir |
| Frecuencia de notificación | **Semanal por defecto** (configurable a futuro) | ✅ |

> Frecuencia: para el MVP se mantiene **semanal** (coherente con `notificaciones.md`).
> Diario/quincenal queda como opción futura.

---

## 3. Credencial verificable (URL compartible) — opt-in

Cada estudiante/egresado puede **activar** una **carta de presentación verificada por la UNSA**
con URL compartible. **No es un perfil social** (respeta el "NO perfiles públicos / NO red social"
de `paginas.md`): es un **artefacto de verificación**, no una red.

### Diferencia clave (compatible con el guardrail)
| ❌ Perfil social (prohibido) | ✅ Credencial verificable (esto) |
|---|---|
| Buscable / indexable | **Solo por link** que el dueño comparte |
| Cualquiera explora perfiles | Nadie explora; necesitas el enlace |
| Feed, conexiones, mensajería | **Sin** features sociales — ficha de solo lectura |

### Condiciones obligatorias (Ley 29733)
- **Opt-in, apagado por defecto** — nadie tiene URL sin activarla.
- **Control granular** — el dueño elige qué credenciales muestra.
- **`noindex`** — no indexable por buscadores.
- **Link revocable** — se puede apagar cuando quiera.

### Implementación (ligera, reutiliza el perfil)
- Switch *"Activar mi carta de presentación"* → genera URL `/credencial/<slug>`.
- Página de **solo lectura**, sin features sociales.
- En el pitch: *"cada egresado obtiene una credencial profesional verificada por la UNSA —
  no es red social, es una carta de presentación que el egresado decide compartir."*

---

## 4. Resumen de decisiones

| Punto | Decisión |
|---|---|
| Perfil en demo | Editable (autodeclarado); 3 perfiles de muestra sembrados como verificados |
| Dos orígenes | 🟢 verificado (sync) solo lectura · ⚪ autodeclarado editable |
| Preferencias | Carrera fija + afines extra + silenciar + tipos preferidos + frecuencia |
| Frecuencia | Semanal (configurable a futuro) |
| Credencial | URL opt-in, no social, noindex, revocable, control granular |
