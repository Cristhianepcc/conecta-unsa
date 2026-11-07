"""Casos funcionales de acceso al flujo de convocatorias (Issue #10)."""

from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from apps.empresas.models import ESTADO_ACTIVA, Empresa, Reclutador
from apps.usuarios.models import ROL_RECLUTADOR

from .test_selenium_base import SeleniumFunctionalTestCase

User = get_user_model()


class ConvocatoriaAccessFunctionalTests(SeleniumFunctionalTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.empresa = Empresa.objects.create(
            ruc="20777777777",
            razon_social="Empresa Funcional SAC",
            estado=ESTADO_ACTIVA,
        )
        cls.user = User.objects.create_user(
            username="selenium_reclutador",
            password="claveSegura123",
        )
        cls.user.set_password("claveSegura123")
        cls.user.save(update_fields=["password"])
        cls.user.perfil.rol = ROL_RECLUTADOR
        cls.user.perfil.save(update_fields=["rol"])
        Reclutador.objects.create(
            usuario=cls.user,
            empresa=cls.empresa,
            nombres="Luis",
            ap_paterno="Funcional",
        )

    def _iniciar_sesion_como_empresa(self):
        self.client.force_login(type(self).user)
        self.driver.get(self.live_server_url)
        self.driver.add_cookie(
            {
                "name": "sessionid",
                "value": self.client.cookies["sessionid"].value,
                "path": "/",
            }
        )
        self.driver.get(f"{self.live_server_url}/empresas/dashboard/")
        WebDriverWait(self.driver, 10).until(EC.url_contains("/empresas/dashboard/"))

    def test_usuario_anonimo_es_redirigido_al_login(self):
        self.driver.get(f"{self.live_server_url}/empresas/publicar/")

        WebDriverWait(self.driver, 10).until(EC.url_contains("/usuarios/login/"))
        self.assertIn("/usuarios/login/", self.driver.current_url)

    def test_reclutador_autenticado_ve_formulario_de_convocatoria(self):
        self._iniciar_sesion_como_empresa()
        self.driver.get(f"{self.live_server_url}/empresas/publicar/")

        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Publicar convocatoria")
        )
        self.assertIn("Publicar convocatoria", self.driver.page_source)
        self.assertTrue(self.driver.find_element(By.TAG_NAME, "form").is_displayed())
