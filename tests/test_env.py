import logging
import os
import sys


from dotenv import load_dotenv

log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level="NOTSET", format=log_format, datefmt="[%X]")

load_dotenv()

token = os.getenv("token")
logging.info(f"Token:{token}")

try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    print(f"{GEMINI_API_KEY}")
    logging.info("Başarılı")
except KeyError:
    logging.info("HATA")
    sys.exit(1)
