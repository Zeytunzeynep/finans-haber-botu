from content_bot.models.news import News
from content_bot.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class BloombergPage(BasePage):

    bloomberg_links = (By.CSS_SELECTOR, "a:has(figure)")

    base_url = "https://www.bloomberght.com"
    cate_url = "https://www.bloomberght.com/ekonomi"

    # sonradan eklenen locatorlar

    article_title = (By.CSS_SELECTOR, "h1.title")
    article_body = (By.CSS_SELECTOR, ".article-wrapper p")

    def load(self):
        self.open_url(self.cate_url)

    def get_article_urls(self) -> list[str]:
        elements = self.find_all(self.bloomberg_links)

        full_urls = []
        print(f"Sayfada {len(elements)} adet haber bulundu")

        for elem in elements:
            relative_link = elem.get_attribute("href")

            if not relative_link:
                continue

            if relative_link.startswith("http"):
                full_urls.append(relative_link)
            else:
                full_urls.append(self.base_url + relative_link)

        return full_urls

    def get_news_details(self) -> News:
        title_element = self.find(self.article_title)
        title_text = title_element.text

        paragraph_elements = self.find_all(self.article_body)

        paragraphs = [p.text for p in paragraph_elements if p.text.strip() != ""]

        full_content = "\n\n".join(paragraphs)

        return News(
            title=title_text,
            content=full_content,
            url=self.driver.current_url,
            source="BloombergHT",
        )
