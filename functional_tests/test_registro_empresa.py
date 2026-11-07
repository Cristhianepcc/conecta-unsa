"""Casos funcionales del registro de empresa (Issue #9)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .test_selenium_base import SeleniumFunctionalTestCase


class RegistroEmpresaFunctionalTests(SeleniumFunctionalTestCase):
    def _completar_registro(self, ruc="20123456789"):
        valores = {
            "ruc": ruc,
            "razon_social": "Empresa Selenium S.A.C.",
            "nombre_comercial": "Empresa Selenium",
            "tipo": "sac",
            "nombres": "Ana",
            "ap_paterno": "Pruebas",
            "dni": "12345678",
            "cargo": "Reclutadora",
            "email": "ana.selenium@example.com",
            "username": "selenium_empresa",
            "password1": "claveSegura123",
            "password2": "claveSegura123",
        }
        for campo, valor in valores.items():
            self.driver.find_element(By.NAME, campo).send_keys(valor)

    def test_registro_valido_muestra_confirmacion(self):
        self.driver.get(f"{self.live_server_url}/empresas/registro/")
        self._completar_registro()
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(self.driver, 10).until(EC.url_contains("/empresas/registro/exito/"))
        self.assertIn("/empresas/registro/exito/", self.driver.current_url)
        self.assertIn("¡Registro enviado!", self.driver.page_source)

    def test_ruc_invalido_mantiene_formulario_y_muestra_error(self):
        self.driver.get(f"{self.live_server_url}/empresas/registro/")
        self._completar_registro(ruc="1234567890")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "El RUC debe tener 11 dígitos.")
        )
        self.assertIn("/empresas/registro/", self.driver.current_url)
        self.assertNotIn("/empresas/registro/exito/", self.driver.current_url)
        self.assertIn("El RUC debe tener 11 dígitos.", self.driver.page_source)
