from content_bot.models.news import News
from content_bot.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class EkonomimPage(BasePage):

    # --- LOCATORS ---
    ekonomim_links = (By.CSS_SELECTOR, "a.box")
    title_locator = (By.CSS_SELECTOR, "h1")
    body_locator = (By.CSS_SELECTOR, ".content-text p")

    base_url = "https://www.ekonomim.com/ekonomi"

    def load(self):
        self.open_url(self.base_url)

    def get_article_urls(self) -> list[str]:
        elements = self.find_all(self.ekonomim_links)
        eko_link = []

        print(f"🔎 Ekonomim.com üzerinde {len(elements)} haber kutusu bulundu.")

        for elem in elements:
            link = elem.get_attribute("href")
            if link and link.startswith("http"):
                eko_link.append(link)

        return list(set(eko_link))

    def get_news_details(self) -> News:
        # --- 1. GÜVENLİK KİLİDİ (EN ÖNEMLİ KISIM BURASI) ---
        # Değişkenleri en başta tanımlıyoruz ki aşağıda "yok" demesin.
        title_text = "Başlık Bulunamadı"
        full_content = "İçerik Bulunamadı"
        current_url = self.driver.current_url

        # --- 2. BAŞLIK ÇEKME ---
        try:
            # Başlık var mı kontrol et
            if self.driver.find_elements(*self.title_locator):
                title_text = self.driver.find_element(*self.title_locator).text.strip()
            else:
                # Yoksa alternatif ara
                titles = self.driver.find_elements(By.CLASS_NAME, "title")
                if titles:
                    title_text = titles[0].text.strip()
        except Exception as e:
            print(f"   ⚠️ Başlık hatası: {e}")

        # --- 3. İÇERİK ÇEKME ---
        try:
            paragraph_elements = self.driver.find_elements(*self.body_locator)

            # Eğer class ile bulamazsan ID ile dene
            if not paragraph_elements:
                paragraph_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, "#content p"
                )

            # Metinleri al
            paragraphs = [p.text for p in paragraph_elements if p.text.strip() != ""]

            # Eğer liste doluysa birleştir, boşsa dokunma (yukarıdaki "İçerik Bulunamadı" kalır)
            if paragraphs:
                full_content = "\n\n".join(paragraphs)

        except Exception as e:
            print(f"   ⚠️ İçerik hatası: {e}")

        # --- 4. PAKETLEME VE GÖNDERME ---
        # Artık title_text ve full_content kesinlikle var (ya dolu ya da varsayılan metin)
        return News(
            title=title_text,
            content=full_content,
            url=current_url,
            source="Ekonomim",
            author="Ekonomim",
        )
