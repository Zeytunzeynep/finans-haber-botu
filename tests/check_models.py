import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env yükle
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API Key yok! .env dosyasını kontrol et.")
else:
    print(f"🔑 API Key bulundu: {api_key[:5]}*******")

    try:
        genai.configure(api_key=api_key)

        print("\n🔍 Google'a soruluyor: 'Hangi modeller açık?'...")
        print("-" * 40)

        # Modelleri listele
        found_any = False
        for m in genai.list_models():
            # Sadece metin üretme (generateContent) yeteneği olanları göster
            if "generateContent" in m.supported_generation_methods:
                print(f"✅ BULUNDU: {m.name}")
                found_any = True

        if not found_any:
            print("⚠️ Hiçbir model bulunamadı. API Key veya Bölge sorunu olabilir.")

        print("-" * 40)

    except Exception as e:
        print(f"❌ HATA: {e}")
