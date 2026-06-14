"""Tests de la feature 12-panel-admin (criterios EARS)."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.convocatorias.models import (
    ESTADO_OBSERVADA,
    ESTADO_PENDIENTE,
    ESTADO_PUBLICADA,
    Convocatoria,
)
from apps.core import constants
from apps.core.models import AdminAllowlist
from apps.empresas.models import ESTADO_ACTIVA, Empresa
from apps.taxonomia.models import Carrera
from apps.usuarios.services import resolver_rol

User = get_user_model()


class BasePanel(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_config")
        call_command("seed_taxonomia")
        call_command("seed_elegibilidad")
        cls.empresa = Empresa.objects.create(
            ruc="23000000001", razon_social="Panel SAC", estado=ESTADO_ACTIVA
        )
        cls.sistemas = Carrera.objects.get(nombre="Ingeniería de Sistemas")

    def _conv(self, titulo="Empleo", estado=ESTADO_PENDIENTE, **kw):
        conv = Convocatoria.objects.create(
            empresa=self.empresa, tipo=constants.TIPO_EMPLEO, titulo=titulo,
            descripcion="x" * 120, modalidad="remoto", ubicacion="AQP",
            duracion_estimada="6m", fecha_limite=date.today() + timedelta(days=20),
            medio_postulacion="https://x.pe", email_contacto="a@x.pe",
            no_discriminacion=True, regimen="728", estado=estado, transparencia_pct=70, **kw,
        )
        conv.carreras_objetivo.set([self.sistemas])
        return conv

    def _admin(self):
        AdminAllowlist.objects.create(email="jefe@unsa.edu.pe")
        user = User.objects.create_user("jefe", email="jefe@unsa.edu.pe", password="x")
        resolver_rol(user)
        self.client.force_login(user)
        return user

    def _egresado(self):
        user = User.objects.create_user("ana", email="ana@gmail.com", password="x")
        self.client.force_login(user)
        return user


class AccesoTests(BasePanel):
    def test_ca6__no_admin_denegado(self):
        """CA-6: un usuario sin rol admin no entra al panel (403)."""
        self._egresado()
        resp = self.client.get(reverse("core:panel_admin"))
        self.assertEqual(resp.status_code, 403)

    def test_ca6__admin_entra(self):
        self._admin()
        self.assertEqual(self.client.get(reverse("core:panel_admin")).status_code, 200)


class BandejaTests(BasePanel):
    def test_ca1__bandeja_lista_pendientes_con_transparencia(self):
        """CA-1: la bandeja muestra convocatorias por revisar con su % de transparencia."""
        self._conv(titulo="Por revisar")
        self._admin()
        resp = self.client.get(reverse("core:panel_admin"))
        self.assertContains(resp, "Por revisar")
        self.assertContains(resp, "70%")

    def test_ca3__resalta_duplicado(self):
        """CA-3: la bandeja resalta duplicados (misma empresa + título similar)."""
        self._conv(titulo="Analista de Datos")
        self._conv(titulo="Analista de datos")  # similar
        self._admin()
        resp = self.client.get(reverse("core:panel_admin"))
        self.assertContains(resp, "duplicado")


class AccionesTests(BasePanel):
    def test_ca2__aprobar_publica(self):
        conv = self._conv()
        self._admin()
        self.client.post(reverse("core:revisar_convocatoria", args=[conv.id]), {"accion": "aprobar"})
        conv.refresh_from_db()
        self.assertEqual(conv.estado, ESTADO_PUBLICADA)

    def test_ca2__observar_registra_comentario_y_notifica(self):
        """CA-2: observar registra el comentario (y notifica a la empresa si tiene reclutador)."""
        from apps.empresas.models import Reclutador

        recl = User.objects.create_user("recl", email="r@x.pe", password="x")
        Reclutador.objects.create(usuario=recl, empresa=self.empresa, nombres="R", ap_paterno="X")
        conv = self._conv()
        self._admin()
        self.client.post(
            reverse("core:revisar_convocatoria", args=[conv.id]),
            {"accion": "observar", "comentario": "Agrega banda salarial."},
        )
        conv.refresh_from_db()
        self.assertEqual(conv.estado, ESTADO_OBSERVADA)
        self.assertEqual(conv.comentario_revision, "Agrega banda salarial.")
        self.assertTrue(recl.notificaciones.filter(tipo="observada").exists())

    def test_ca2__observar_sin_comentario_no_procede(self):
        conv = self._conv()
        self._admin()
        self.client.post(reverse("core:revisar_convocatoria", args=[conv.id]), {"accion": "observar"})
        conv.refresh_from_db()
        self.assertEqual(conv.estado, ESTADO_PENDIENTE)  # no cambió

    def test_ca2__rechazar(self):
        conv = self._conv()
        self._admin()
        self.client.post(reverse("core:revisar_convocatoria", args=[conv.id]),
                         {"accion": "rechazar", "comentario": "No cumple."})
        conv.refresh_from_db()
        self.assertEqual(conv.estado, "rechazada")


class MetricasTests(BasePanel):
    def test_ca4__metricas_reales(self):
        """CA-4: las métricas se calculan de datos reales."""
        self._conv(titulo="P1", estado=ESTADO_PENDIENTE)
        self._conv(titulo="Pub1", estado=ESTADO_PUBLICADA)
        self._admin()
        resp = self.client.get(reverse("core:panel_admin"))
        self.assertEqual(resp.context["metricas"]["pendientes"], 1)
        self.assertEqual(resp.context["metricas"]["validadas"], 1)
