# Notificaciones — CONECTA UNSA

> El mecanismo anti-saturación de la propuesta: en vez de N correos sueltos, el egresado
> recibe **un único resumen consolidado** (`propuesta.md` §6.4).
> Stack base: *Cron job + correo* (`stack-conecta-unsa.md`).

---

## 1. Frecuencia

- **Resumen semanal.** Coincide con el "Resumen semanal de oportunidades" de la landing y el dashboard.
- Un **cron job** semanal agrupa las convocatorias del período pertinentes a cada egresado
  (según sus carreras/preferencias) y arma un solo correo.
- (Futuro) la frecuencia podría hacerse configurable por el egresado (diario/semanal/quincenal).

---

## 2. Canal de correo — envío real con Resend

Decisión: **envío real (opción b)**, no solo vista previa.

- **Proveedor: Resend** (ya configurado en el entorno; plan gratis 3,000 correos/mes).
- Django envía con su backend de correo nativo (`django.core.mail`) vía API/SMTP de Resend.
- **Dominio de prueba propio** (lo tiene el usuario) → se **verifica en Resend** para:
  - remitente profesional (ej. `noreply@<dominio-prueba>`),
  - mejor entregabilidad (menos probabilidad de caer en spam).
- Credenciales (`RESEND_API_KEY`, remitente) van como **variables de entorno en Railway**, nunca en el código.

**Plantilla reutilizable:** el resumen es una sola plantilla HTML. Aunque el envío es real,
esa misma plantilla puede renderizarse como vista previa en el dashboard si se quiere mostrar
sin enviar. "Enviar" es solo activar el backend de correo.

### Pendiente para el despliegue
- [ ] Nombre del dominio de prueba (para verificarlo en Resend).
- [ ] Configurar registros DNS (SPF/DKIM) del dominio en Resend (~15 min).

---

## 3. Notificaciones dentro de la plataforma

- **Sí**, se incluye un **centro de notificaciones (campana 🔔)** en el dashboard del egresado.
- Muestra avisos in-app: nuevas convocatorias pertinentes, recordatorios de fechas límite,
  resumen disponible, etc. — complementa (no reemplaza) el correo semanal.

---

## 4. Resumen de decisiones

| Punto | Decisión |
|---|---|
| Frecuencia | Semanal (cron job) |
| Canal | Correo real vía **Resend** + dominio de prueba verificado |
| Vista previa in-app | Opcional (misma plantilla), no es el canal principal |
| Campana in-app | Sí |
| Secretos | En variables de entorno de Railway |
