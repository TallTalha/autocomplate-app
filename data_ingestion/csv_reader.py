# autocomplete-app/data_ingestion/csv_reader.py
"""
Bu modül, kaynak veri dosyalarını (örn: CSV) okuyup, Elasticsearch'e
yüklenecek formata dönüştüren generator fonksiyonlarını içerir.
"""
import csv
import logging

LOG = logging.getLogger(__name__)

def generate_actions_from_csv(csv_path: str, index_name:str):
    """
    Açıklama:
        CSV dosyasını satır satır okur ve Elasticsearch bulk API'sinin
        anlayacağı formatta "action" objeleri üretir (yield).
    Args:
        csv_path(str): CSV dosyasının dizini.
        index_name(str): Verilerin indeksleneceği indeks.
    Returns:
        None
    """
    LOG.info(f"'{csv_path}' dosyasından bulk actions hazırlanıyor...")

    try:
        with open(csv_path, mode='r', encoding='utf-8') as c:
            reader = csv.DictReader(c)
            for row in reader:
                yield{
                    "_index": index_name,
                    "_source": row
                }
    except FileNotFoundError as e:
        LOG.critical(f"{csv_path} dizininde dosya mevcut değil.")
        raise
    except Exception as e:
        LOG.critical(f"CSV dosyasından bulk aksiyonları oluştururken hata: {e}", exc_info=True)
        raise