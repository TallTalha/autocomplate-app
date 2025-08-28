# autocomplete-app/data_ingestion/run_ingestion.py
"""
Autocomplete projesi için CSV'den Elasticsearch'e veri yükleme
iş akışını (ETL) yöneten ana script.
"""
import os
import sys
import logging
from .configs.ingestion_config import ELASTIC_URL, ELASTIC_USER, ELASTIC_PASSWORD, ELASTIC_FINGERPRINT, ELASTIC_INDEX_NAME

app_dir = os.path.dirname(os.path.abspath(__file__)) # autocomplete-app/data_ingestion
project_root = os.path.dirname(app_dir)
sys.path.append(project_root)

CSV_FILE = os.path.join(project_root,"data","product.csv")

MAPPING_BODY = {
    "searching":{
        "analysis":{
            "filter":{
                "autocomplete_edge_ngram_filter":{
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 10,
                }
            },
            "analyzer":{
                "autocomplete_analyzer":{
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter":[
                        "lowercase",
                        "autocomplete_edge_ngram_filter"
                    ]
                }
            }
        }
    },
    "mapping":{
        "properties":{
            "title":{
                "type": "text",
                "analyzer": "autocomplete_analyzer",
                "search_analyzer": "standard"
            },
            "category":{
                "type": "keyword"
            },
            "brand": {
                "type": "keyword"
            }
        }
    }
}

from utils.logger import setup_logger

setup_logger(name="data_ingestion", app_dir=app_dir)

from elasticsearch.helpers import bulk
from data_ingestion.es_connector import get_es_client, create_index_if_not_exists
from data_ingestion.csv_reader import generate_actions_from_csv

def main():
    """Ana ETL iş akışını yönetir."""
    LOG = logging.getLogger(__name__)
    LOG.info("Autocomplete veri yükleme script'i başlatıldı.")

    es_client = get_es_client(ELASTIC_URL, ELASTIC_USER, ELASTIC_PASSWORD, ELASTIC_FINGERPRINT)
    if not es_client:
        sys.exit(1) # -> ÇIKIŞ
    
    try:
        create_index_if_not_exists(es_client, ELASTIC_INDEX_NAME, MAPPING_BODY)

        LOG.info("Bulk veri yükleme işlemi başlatılıyor...")
        success, errors = bulk(
            es_client,
            generate_actions_from_csv(CSV_FILE, ELASTIC_INDEX_NAME),
            raise_on_error=False
        )
        LOG.info(f"Bulk işlemi tammamlandı. Başarılı:{success}, Hatalı:{len(errors)}")
        if errors:
            LOG.warning(f"İlk 5 yükleme hatası{errors[:5]}")
    except Exception as e:
        LOG.critical(f"Ingestion iş akışında beklenmedik bir hata oluştu: {e}", exc_info=True)
        sys.exit(1) # -> ÇIKIŞ
    
    LOG.info("Ingestion iş akışı başarıyla tammamlandı.")

if __name__ == "__main__":
    main()