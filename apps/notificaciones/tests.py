"""Tests de la feature 08-notificaciones (criterios EARS)."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.test import TestCase

from apps.core import constants
from apps.convocatorias.models import ESTADO_PUBLICADA, Convocatoria
from apps.empresas.models import ESTADO_ACTIVA, Empresa
from apps.taxonomia.models import Carrera
from apps.usuarios.models import PerfilTalento

from . import services
from .models import Notificacion, ResumenSemanalLog, TIPO_OBSERVADA

User = get_user_model()


class BaseNotif(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_config")
        call_command("seed_taxonomia")
        call_command("seed_elegibilidad")
        cls.empresa = Empresa.objects.create(
            ruc="20800000001", razon_social="Notif SAC", estado=ESTADO_ACTIVA
        )
        cls.sistemas = Carrera.objects.get(nombre="Ingeniería de Sistemas")

    def _conv(self, tipo=constants.TIPO_EMPLEO, titulo="Empleo", carreras=None):
        conv = Convocatoria.objects.create(
            empresa=self.empresa, tipo=tipo, titulo=titulo, estado=ESTADO_PUBLICADA,
            fecha_limite=date.today() + timedelta(days=20), transparencia_pct=80,
        )
        conv.carreras_objetivo.set(carreras or [self.sistemas])
        return conv

    def _egresado(self, username="egre", carrera=None, estado="egresado", frecuencia="semanal"):
        user = User.objects.create_user(
            username, email=f"{username}@gmail.com", password="x", first_name="Ana"
        )
        talento, _ = PerfilTalento.objects.get_or_create(usuario=user)
        talento.carrera = carrera or self.sistemas
        talento.estado_academico = estado
        talento.frecuencia = frecuencia
        talento.save()
        return user


class ResumenTests(BaseNotif):
    def test_ca1_ca2__un_solo_correo_con_pertinentes(self):
        """CA-1/CA-2: un único correo por egresado con sus convocatorias pertinentes."""
        self._conv(titulo="Empleo A")
        self._conv(titulo="Empleo B")
        user = self._egresado()
        mail.outbox = []
        enviado = services.enviar_resumen_a(user)
        self.assertTrue(enviado)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [user.email])
        self.assertIn("Empleo A", mail.outbox[0].body)

    def test_ca3__sin_novedades_no_envia(self):
        """CA-3: sin convocatorias nuevas, no se envía correo."""
        self._conv(titulo="Empleo A")
        user = self._egresado()
        self.assertTrue(services.enviar_resumen_a(user))  # primera vez sí
        mail.outbox = []
        self.assertFalse(services.enviar_resumen_a(user))  # ya las recibió → no reenvía
        self.assertEqual(len(mail.outbox), 0)

    def test_ca4__respeta_silenciadas(self):
        """CA-4: respeta las categorías silenciadas del perfil."""
        self._conv(tipo=constants.TIPO_VOLUNTARIADO, titulo="Voluntariado X")
        user = self._egresado()
        user.perfil_talento.categorias_silenciadas = [constants.TIPO_VOLUNTARIADO]
        user.perfil_talento.save()
        convs = services.construir_resumen(user)
        self.assertEqual(convs, [])

    def test_ca4__frecuencia_ninguna_no_envia(self):
        self._conv(titulo="Empleo A")
        user = self._egresado(frecuencia="ninguna")
        self.assertFalse(services.enviar_resumen_a(user))

    def test_ca6__registra_log(self):
        """CA-6: cada envío se registra para auditoría."""
        self._conv(titulo="Empleo A")
        user = self._egresado()
        services.enviar_resumen_a(user)
        self.assertEqual(ResumenSemanalLog.objects.filter(usuario=user).count(), 1)

    def test__comando_enviar_resumenes(self):
        self._conv(titulo="Empleo A")
        self._egresado()
        mail.outbox = []
        call_command("enviar_resumenes")
        self.assertEqual(len(mail.outbox), 1)


class InAppTests(BaseNotif):
    def test_ca5__evento_crea_notificacion_inapp(self):
        """CA-5: un evento relevante crea una notificación in-app."""
        user = self._egresado()
        services.notificar(user, "Nueva convocatoria para ti", tipo="nueva_pertinente")
        self.assertEqual(Notificacion.objects.filter(usuario=user, leido=False).count(), 1)
        self.assertEqual(services.no_leidas(user), 1)

    def test_ca5__observacion_notifica_a_empresa(self):
        """CA-5/CA-6 (06): observar una convocatoria notifica al reclutador."""
        from apps.empresas.models import Reclutador
        from apps.convocatorias import flujo
        from apps.convocatorias.models import ESTADO_PENDIENTE

        recl_user = User.objects.create_user("recl", email="recl@x.pe", password="x")
        Reclutador.objects.create(
            usuario=recl_user, empresa=self.empresa, nombres="R", ap_paterno="X"
        )
        conv = self._conv(titulo="Para observar")
        conv.estado = ESTADO_PENDIENTE
        conv.save()
        flujo.observar(conv, "Corrige la banda salarial.")
        self.assertTrue(
            Notificacion.objects.filter(usuario=recl_user, tipo=TIPO_OBSERVADA).exists()
        )

    def test__marca_leidas_al_abrir(self):
        user = self._egresado()
        services.notificar(user, "Aviso")
        self.client.force_login(user)
        self.client.get("/notificaciones/")
        self.assertEqual(services.no_leidas(user), 0)


class MensajesInstitucionalesTests(BaseNotif):
    """Bandeja institucional: canal dedicado a comunicados oficiales (P1)."""

    def _egresado(self, username="eg", estado="egresado"):
        user = User.objects.create_user(username, email=f"{username}@gmail.com", password="x")
        talento, _ = PerfilTalento.objects.get_or_create(usuario=user)
        talento.carrera = self.sistemas
        talento.estado_academico = estado
        talento.save()
        return user

    def test__solo_muestra_los_institucionales(self):
        """La bandeja institucional solo lista mensajes de tipo general; ignora operativos."""
        user = self._egresado()
        services.notificar(user, "Comunicado oficial UNSA", tipo="general")
        services.notificar(user, "Nueva convocatoria para ti", tipo="nueva_pertinente")
        self.client.force_login(user)
        resp = self.client.get("/notificaciones/institucionales/")
        self.assertEqual(resp.status_code, 200)
        # La bandeja solo contiene comunicados (tipo general); ignora los operativos.
        mensajes = resp.context["mensajes"]
        self.assertEqual([m.mensaje for m in mensajes], ["Comunicado oficial UNSA"])

    def test__abrir_marca_leidos_los_institucionales(self):
        """Al abrir la bandeja, los comunicados quedan marcados como leídos."""
        user = self._egresado()
        services.notificar(user, "Comunicado oficial UNSA", tipo="general")
        self.client.force_login(user)
        self.client.get("/notificaciones/institucionales/")
        self.assertEqual(
            Notificacion.objects.filter(usuario=user, tipo="general", leido=False).count(), 0
        )
