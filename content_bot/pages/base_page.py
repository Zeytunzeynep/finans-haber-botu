from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Tuple


class BasePage:
    """Tüm sayfa sınıflarının miras alacağı ebeveyn sınıf."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Explicit Wait tanımlıyoruz (Max 10 sn bekler)
        self.wait = WebDriverWait(driver, 10)

    def open_url(self, url: str):
        """Sayfaya gitme işini standardize ediyoruz."""
        self.driver.get(url)

    def find_all(self, locator: Tuple[str, str]) -> List:
        """
        Element listesi döner.
        Önce elementlerin var olmasını bekler (Wait), sonra bulur.
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def find(self, locator: Tuple[str, str]):
        """Tek bir element bulur."""
        return self.wait.until(EC.visibility_of_element_located(locator))
