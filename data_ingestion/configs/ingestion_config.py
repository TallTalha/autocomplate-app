from dotenv import load_dotenv
import os

load_dotenv()

# Elastich Search Bağlantı Ayarları
ELASTIC_HOST = str(os.getenv('ELASTIC_HOST'))
ELASTIC_PORT = str(os.getenv('ELASTIC_PORT'))
ELASTIC_URL = f"https://{ELASTIC_HOST}:{ELASTIC_PORT}"
ELASTIC_USER = str(os.getenv('ELASTIC_USER'))
ELASTIC_PASSWORD =  str(os.getenv('ELASTIC_PASSWORD'))
ELASTIC_FINGERPRINT = str(os.getenv('ELASTIC_FINGERPRINT'))

# Elastich Search Parametreleri
ELASTIC_INDEX_NAME = "autocompleteapp"