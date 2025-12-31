import google.generativeai as gg
from dotenv import load_dotenv
import os


load_dotenv()


class AiAgent:
    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Anahtar bulunamadı dosyasınızı kontrol edin")

        try:
            gg.configure(api_key=self.api_key)

            self.model = gg.GenerativeModel("gemini-flash-latest")
        except Exception as e:
            print(f"Goggle API hatası: {e}")

    def analyze_news(self, title: str, content: str) -> dict:

        prompt = f"""Sen uzman bir finans analistisin. Aşağıdaki haberi analiz et.

        HABER BAŞLIĞI: {title}
        HABER İÇERİĞİ: {content}

        GÖREVLERİN:
        1. Haberi Türkçe olarak, en fazla 3 maddede özetle.
        2. Bu haberin piyasalara etkisi (Sentiment) nedir? Sadece şu 3 kelimeden birini seç: "OLUMLU", "OLUMSUZ", "NÖTR".

        CEVAP FORMATI:
        Cevabını tam olarak aşağıdaki kalıpta ver (başka bir şey yazma):
        SENTIMENT: [Buraya Duygu Durumu]
        SUMMARY: [Buraya Özet]
        """
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            sentiment = "NÖTR"
            summary = "Özet çıkaralamdı"

            if "SENTIMENT:" in text and "SUMMARY:" in text:
                parts = text.split("SUMMARY:")

                sentiment_part = parts[0].replace("SENTIMENT:", "").strip()
                summary_part = parts[1].strip()

                sentiment = sentiment_part
                summary = summary_part

            else:
                # Eğer AI formatı bozarsa, tüm cevabı özet kabul et
                summary = text

            # 7. Sonucu paketle ve gönder
            return {"sentiment": sentiment, "summary": summary}

        except Exception as e:
            print(f"   ❌ AI Analiz Hatası: {e}")
            # Hata olursa program çökmesin, boş dönsün

            return None
