# Haber sayfalarından çekilen veriyi database'de kontrol etmek için yazılan kod
import sqlite3


conn = sqlite3.connect("news_agent.db")
cursor = conn.cursor()

try:
    cursor.execute("SELECT id, source, title FROM news")
    haberler = cursor.fetchall()

    print(f"\n📂 Veritabanında Toplam {len(haberler)} Haber Var:\n")
    print("-" * 60)

    for haber in haberler:

        print(f"ID: {haber[0]} | [{haber[1]}] -> {haber[2][:50]}...")

    print("-" * 60)

except Exception as e:
    print("Hata:", e)

finally:
    conn.close()
