import os
from jinja2 import FileSystemLoader, Environment
from datetime import datetime


class Reporter:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_dir, "templates")

        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_newsletter(self, news_list):

        try:
            template = self.env.get_template("newsletter.html")
            date = datetime.now().strftime("%d.%m.%Y")

            html_content = template.render(haberler=news_list, tarih=date)

            output_file = "Gunluk_Bulten.html"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            print("Rapor oluşturuldu:{output_file}")
            return html_content

        except Exception as e:
            print(f"Rapor oluşturulamadı:{e}")
            return None
