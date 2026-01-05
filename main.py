from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

from database import DataBase
from content_bot.ai_agent import AiAgent
from content_bot.reporter import Reporter
from content_bot.email_service import EmailService

from content_bot.pages.bloomberg_page import BloombergPage
from content_bot.pages.ekonomim_page import EkonomimPage
from content_bot.pages.doviz_page import DovizPage
from content_bot.pages.haberturk_page import HaberturkPage


def debug_secrets():
    print("--- 🕵️‍♂️ DEBUG BAŞLANGICI ---")

    # 1. Ortamda hangi anahtarlar var? (Sadece isimleri yazdırır)
    env_keys = list(os.environ.keys())
    print(f"Mevcut Değişkenler: {[k for k in env_keys if 'API' in k or 'GEMINI' in k]}")

    # 2. Bizim anahtar orada mı?
    key = os.getenv("GEMINI_API_KEY")

    if key is None:
        print(
            "❌ DURUM: os.getenv('GEMINI_API_KEY') --> None dönüyor (Python değişkeni hiç görmüyor)."
        )
    elif key == "":
        print("❌ DURUM: Değişken var ama içi BOŞ (Empty String).")
    else:
        print(f"✅ DURUM: Anahtar yakalandı! Uzunluk: {len(key)} karakter.")
        print(f"   İlk 2 harf: {key[:2]}*** (AI ile başlamalı)")

    print("--- 🕵️‍♂️ DEBUG BİTİŞİ ---")


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Arayüzsüz mod (Kritik!)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    db = DataBase("news_agent.db")

    ai_brain = None
    reporter = None
    email_service = None

    try:
        ai_brain = AiAgent()
        reporter = Reporter()
        email_service = EmailService()

        print("Beyin çalışıyor")
    except Exception as e:
        print(f"ai başlatılamadı {e}")
        # 4 SAĞLAM KAYNAK
    sources = [
        BloombergPage(driver),
        EkonomimPage(driver),
        DovizPage(driver),
        HaberturkPage(driver),
    ]

    print(f"🚀 Haberler taranıyor")

    for page in sources:
        try:
            page.load()
            time.sleep(2)

            urls = page.get_article_urls()

            for url in urls:
                driver.get(url)
                time.sleep(1.5)

                news = page.get_news_details()

                if news.title != "Başlık Yok" and len(news.content) > 50:
                    db.add_news(news)
                    print(f"Kaydedildi")

        except Exception as e:
            print(f"   ❌ Haber Hatası: {e}")

    driver.quit()

    if ai_brain:
        print("\n🧠 Analiz İşlemi Kontrol Ediliyor...")

        # --- ANALİZ KISMI (Eski kodun aynısı) ---
        unprocessed_news = db.get_unprocessed_news()[:5]
        if unprocessed_news:
            print(f"   ⏳ {len(unprocessed_news)} adet yeni haber analiz edilecek.")
            for index, (news_id, title, content) in enumerate(unprocessed_news, 1):
                print(f"   [{index}/{len(unprocessed_news)}] Analiz: {title[:30]}...")
                result = ai_brain.analyze_news(title, content)

                if result:
                    db.update_new_analysis(
                        news_id, result["summary"], result["sentiment"]
                    )
                    print(f"      ✅ Bitti! (Yön: {result['sentiment']})")
                time.sleep(4)
        else:
            print("   ✅ Analiz edilecek yeni haber yok.")

        # --- YENİ EKLENEN KISIM: RAPORLAMA ---
        print("\n📰 Rapor Hazırlanıyor...")

        # 1. Veritabanından bitmiş haberleri çek
        analyzed_news = db.get_analyzed_news()

        if analyzed_news:
            # 2. Reporter'a gönder ve HTML oluştur
            html_content = reporter.generate_newsletter(analyzed_news)

            if html_content:
                email_service.send_mail(
                    "Finans Bülteni", html_content, "zeynepzeytun.2002@gmail.com"
                )
            print("🏁 SÜREÇ TAMAMLANDI! 'GUNLUK_BULTEN.html' dosyasını kontrol et.")
        else:
            print("⚠️ Raporlanacak veri bulunamadı.")

    db.close()


if __name__ == "__main__":
    debug_secrets()
    main()
