"""Base de pruebas funcionales con Selenium (Issue #8)."""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumFunctionalTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


class PublicHomeFunctionalTests(SeleniumFunctionalTestCase):
    def test_visit_homepage_displays_project_name(self):
        self.driver.get(f"{self.live_server_url}/")

        self.assertIn("CONECTA UNSA", self.driver.title)
        self.assertIn("CONECTA UNSA", self.driver.page_source)
