from content_bot.models.news import News
from content_bot.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class HaberturkPage(BasePage):

    START_URL = "https://www.haberturk.com/ekonomi"

    # --- LOCATORS ---
    # Vitrin Linkleri
    NEWS_LINKS = (By.CSS_SELECTOR, "div[data-name='news'] a")

    # Detay Sayfası Başlık
    TITLE_LOCATOR = (By.CSS_SELECTOR, "h1")

    # Detay İçerik (STRATEJİK LİSTE)
    # Senin attığın resimdeki 'wrapper overflow-hidden' yapısını en başa ekledik!
    CONTENT_LOCATORS = [
        (
            By.CSS_SELECTOR,
            ".wrapper.overflow-hidden",
        ),  # 1. Senin bulduğun yapı (En güçlü aday)
        (By.CLASS_NAME, "content-text"),  # 2. Standart yapı
        (By.CLASS_NAME, "description"),  # 3. Alternatif
        (By.CSS_SELECTOR, "article"),  # 4. Genel makale etiketi
        (By.CSS_SELECTOR, ".news-detail-content"),  # 5. Yedek
    ]

    def load(self):
        if not self.START_URL:
            return
        self.open_url(self.START_URL)

    def get_article_urls(self) -> list[str]:
        elements = self.find_all(self.NEWS_LINKS)
        urls = []

        print(f"🔎 Habertürk üzerinde {len(elements)} haber kartı bulundu.")

        for elem in elements:
            link = elem.get_attribute("href")
            if link:
                # Habertürk bazen '/ekonomi/...' gibi yarım link veriyor, düzeltiyoruz
                if not link.startswith("http"):
                    link = "https://www.haberturk.com" + link
                urls.append(link)

        return list(set(urls))

    def get_news_details(self) -> News:
        # 1. Varsayılan Değerler (DB hatası almamak için String atıyoruz)
        title_text = "Başlık Yok"
        full_content = "İçerik Çekilemedi"
        current_url = self.driver.current_url

        # 2. Başlığı Çek
        try:
            if self.driver.find_elements(*self.TITLE_LOCATOR):
                title_text = self.driver.find_element(*self.TITLE_LOCATOR).text.strip()
        except:
            pass

        # 3. İçeriği Çek (ÇOKLU KİLİT SİSTEMİ)
        found_content = False

        for locator in self.CONTENT_LOCATORS:
            try:
                # Önce ana kutuyu bul (wrapper, content-text vb.)
                container_list = self.driver.find_elements(*locator)

                if container_list:
                    container = container_list[0]

                    # Kutunun içindeki tüm <p> etiketlerini al
                    paragraphs = container.find_elements(By.TAG_NAME, "p")

                    # Eğer <p> varsa metinleri birleştir
                    if paragraphs:
                        texts = [p.text for p in paragraphs if p.text.strip() != ""]
                        if texts:
                            full_content = "\n\n".join(texts)
                            found_content = True
                            # print(f"   ✅ İçerik bulundu! (Yöntem: {locator})") # Debug için açabilirsin
                            break  # Bulduk, döngüden çık!

                    # Eğer <p> yoksa ama kutuda metin varsa (bazı eski haberlerde olur)
                    else:
                        text = container.text.strip()
                        if len(text) > 50:
                            full_content = text
                            found_content = True
                            break

            except:
                continue  # Bu yöntem çalışmadı, sıradakine geç

        if not found_content:
            print(f"   ⚠️ İçerik hiçbir yöntemle bulunamadı: {current_url}")

        # 4. Gönder
        return News(
            title=title_text,
            content=full_content,
            url=current_url,
            source="Haberturk",
            author="Haberturk",
        )
