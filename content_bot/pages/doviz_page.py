from content_bot.models.news import News
from content_bot.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class DovizPage(BasePage):

    doviz_links = (By.CSS_SELECTOR, ".news-list a")

    title_locator = (By.CSS_SELECTOR, "h1")

    body_locator = (By.CSS_SELECTOR, ".content p")

    author_locator = (By.CSS_SELECTOR, ".author")

    base_url = "https://haber.doviz.com/"

    def load(self):
        self.open_url(self.base_url)

    def get_article_urls(self) -> list[str]:

        elements = self.find_all(self.doviz_links)

        dv_links = []

        print(f"🔎 Doviz.com üzerinde {len(elements)} haber kartı bulundu.")

        for elem in elements:
            link = elem.get_attribute("href")
            # Link dolu mu ve 'http' ile başlıyor mu?
            if link and link.startswith("http"):
                dv_links.append(link)

        return list(set(dv_links))

    def get_news_details(self) -> News:

        # --- 1. Değişkenleri Hazırla (Güvenlik Önlemi) ---
        title_text = "Başlık Bulunamadı"
        full_content = "İçerik Bulunamadı"
        author_text = "Doviz.com"  # Varsayılan yazar
        current_url = self.driver.current_url

        # --- 2. Başlığı Çek ---
        try:
            if self.driver.find_elements(*self.title_locator):
                title_text = self.driver.find_element(*self.title_locator).text.strip()
        except Exception as e:
            print(f"   ⚠️ Başlık hatası: {e}")

        # --- 3. İçeriği Çek ---
        try:
            # Paragrafları bul
            paragraph_elements = self.driver.find_elements(*self.body_locator)

            # Metinleri al ve birleştir
            paragraphs = [p.text for p in paragraph_elements if p.text.strip() != ""]

            if paragraphs:
                full_content = "\n\n".join(paragraphs)
            else:
                # Eğer p etiketiyle bulamazsa, belki direkt div içindedir
                content_div = self.driver.find_elements(By.CLASS_NAME, "content")
                if content_div:
                    full_content = content_div[0].text

        except Exception as e:
            print(f"   ⚠️ İçerik hatası: {e}")

        # --- 4. Yazarı Çek (Bonus) ---
        try:
            if self.driver.find_elements(*self.author_locator):
                author_text = self.driver.find_element(
                    *self.author_locator
                ).text.strip()
        except:
            pass  # Yazar bulamazsa varsayılan kalsın, sorun yok.

        # --- 5. Paketi Gönder ---
        return News(
            title=title_text,
            content=full_content,
            url=current_url,
            source="DovizCom",  # Kaynak ismini böyle verelim
            author=author_text,
        )
