from content_bot.ai_agent import AiAgent

try:
    ajan = AiAgent()
    print("🧠 Beyin yüklendi. Test ediliyor...")

    sonuc = ajan.analyze_news(
        title="Dolar Rekor Kırdı",
        content="Piyasalarda dolar kuru aniden yükselerek 35 TL seviyesini aştı.",
    )

    print("\n--- SONUÇ ---")
    print(sonuc)

except Exception as e:
    print(f"Hata: {e}")
