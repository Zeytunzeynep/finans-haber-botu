import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

load_dotenv()


class EmailService:
    def __init__(self):
        self.email = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")

        if not self.email or not self.password:
            print("⚠️ HATA: .env dosyasından mail bilgileri okunamadı!")

    def send_mail(self, subject, html_content, receiver_adress):

        ms = MIMEMultipart()
        ms["From"] = self.email
        ms["To"] = receiver_adress
        ms["Subject"] = subject

        ms_text = MIMEText(html_content, "html")
        ms.attach(ms_text)
        print("HTML e-posta taslağı hazır")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.email, self.password)
            server.sendmail(self.email, receiver_adress, ms.as_string())

            print(f"✅ Mail başarıyla gönderildi: {receiver_adress}")
            return True
