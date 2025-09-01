from dotenv import load_dotenv
import os

load_dotenv()

# ES Sunucu Bilgileri
ES_HOST = os.getenv("ELASTIC_HOST")
ES_PORT = os.getenv("ELASTIC_PORT")
ES_URL = f"https://{ES_HOST}:{ES_PORT}"

# ES Kullanıcı Doğrulama Bilgileri
ES_USER = os.getenv("ELASTIC_USER")
ES_PASS = os.getenv("ELASTIC_PASSWORD") 
ES_FINGER = os.getenv("ELASTIC_FINGERPRINT")

# ES Index Bilgileri
ES_INDEX = "autocompleteapp"