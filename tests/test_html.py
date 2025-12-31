import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime


def test_template():
    print("🎨 HTML Şablon Testi Başlıyor...")

    # 1. Şablon Klasörünü Bul
    # src/content_bot/templates klasörüne giden yolu ayarlıyoruz
    base_dir = os.getcwd()  # Projenin ana dizini
    template_dir = os.path.join(base_dir, "content_bot", "templates")

    print(f"📂 Şablon aranıyor: {template_dir}")

    # 2. Jinja2 Motorunu Başlat
    try:
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("newsletter.html")
        print("✅ Şablon bulundu!")
    except Exception as e:
        print(
            f"❌ HATA: Şablon dosyası bulunamadı. Lütfen 'src/content_bot/templates/newsletter.html' dosyasının olduğundan emin ol."
        )
        print(f"Detay: {e}")
        return

    # 3. Sahte Veri Oluştur (Sanki veritabanından gelmiş gibi)
    # Tasarımını görmek için 3 farklı duygu durumunda haber uyduruyoruz
    sahte_haberler = [
        {
            "title": "Borsa İstanbul Rekor Kırdı! 🚀",
            "summary": "1. BIST 100 endeksi günü %5 yükselişle kapattı. 2. Bankacılık hisseleri öncülük etti. 3. Yatırımcıların yüzü güldü.",
            "sentiment": "OLUMLU",
        },
        {
            "title": "Enflasyon Beklentiyi Aştı 📉",
            "summary": "TÜİK verilerine göre yıllık enflasyon %65 seviyesine ulaştı. Merkez Bankası'nın faiz artırması bekleniyor.",
            "sentiment": "OLUMSUZ",
        },
        {
            "title": "Altın Fiyatları Durağan Seyrediyor ⚖️",
            "summary": "Ons altın 2000 dolar seviyesinde dengelenme çabasında. Piyasalar FED kararını bekliyor.",
            "sentiment": "NÖTR",
        },
    ]

    # 4. Şablonu "Pişir" (Render)
    # HTML kodlarının içine verileri yerleştiriyoruz
    bugun = datetime.now().strftime("%d.%m.%Y")
    html_cikti = template.render(haberler=sahte_haberler, tarih=bugun)

    # 5. Sonucu Kaydet
    output_filename = "deneme_bulten.html"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_cikti)

    print("-" * 30)
    print(f"🎉 İŞLEM TAMAM! '{output_filename}' dosyası oluşturuldu.")
    print("Dosyaya çift tıklayıp tarayıcıda tasarımını görebilirsin.")
    print("-" * 30)


if __name__ == "__main__":
    test_template()
