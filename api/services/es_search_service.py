# autocomplete-app/api/services/es_search_service.py
"""Elasticsearch üzerinde autocomplete sorguları çalıştıran servis."""
import logging
from elasticsearch import Elasticsearch
from typing import List, Dict, Any

LOG = logging.getLogger(__name__)

# Bu değişken, lifespan yöneticisi tarafından doldurulacak.
es_client: Elasticsearch | None = None

def fetch_auto_complete_suggestions(index_name: str, query_text: str, size: int = 10) -> List[Dict[str, Any]] | List:
    """
    Açıklama:
        Metin girdisine göre Elasticsearch'ten {size} kadar tamamlama önerisi alır.
    Args:
        index_name(str): Öneri için kullanılacak Elastic search indeksi. 
        query_text(str): Girdi metini.
        size(int): Elasticsearch aracından dönecek öneri adedi.
    Returns:
        suggestions(List[Dict[str, Any]] | List): Öneri varsa içinde sözlük yapısında önerileri içeren bir liste (öneri yoksa boş liste döner),
            hata oluşursa bir LOG hata mesajıyla beraber boş liste döner.
    """
    if not es_client:
        LOG.critical("Elasticsearch istemcisi mevcut değil.")
        return []
    
    try:
        response = es_client.search(
            index = index_name,
            query = {
                "match_phrase_prefix":{
                    "title":{
                        "query": query_text,
                    }
                }
            },
            size = size
        )
        suggestions = [
            hit['_source'] for hit in response['hits']['hits']
        ]
        LOG.info(f"'{query_text}' sorgusu için {len(suggestions)} adet öneri bulundu.")
        return suggestions
    
    except Exception as e:
        LOG.error(f"'{query_text}' için arama yapılırken hata: {e}", exc_info=True)
        return []

