# autocomplete-app/data_ingestion/es_connector.py
"""
Bu modül, Elasticsearch bağlantısını ve indeks yönetimi
fonksiyonlarını merkezileştirir.
"""

import logging
from elasticsearch import Elasticsearch

LOG = logging.getLogger(__name__)

def get_es_client(elastic_url: str, elastic_user: str, elastic_paswd: str, elastic_fingerprint: str) -> Elasticsearch | None:
    """
    Açıklama:
        Elasticsearch'e bağlanır ve  istemci nesnesini döndürür.
    Args:
        elastic_url(str): ´https://{ELASTIC_HOST}:{ELASTIC_PORT}´ formatındaki URL.
        elastic_user(str): Elastichsearch aracında kullanılacak kullanıcı adı.
        elastic_paswd(str): Elastichsearch aracında kullanılacak kullanıcı şifresi.
        elastic_fingerprint(str): Güvenli bağlantı için ´CD:EF:...:34:56´ formatındaki parmak izi.
    Returns:
        es_client(Elasticsearch|None): Bağlantı hatası oluşmazsa ES istemcisi, hata oluşursa None döner.
    """
    LOG.info("Elasticsearch aracına bağlanılıyor... ")
    try:
        es_client = Elasticsearch(
            hosts= [elastic_url],
            basic_auth=(elastic_user, elastic_paswd),
            ssl_assert_fingerprint= elastic_fingerprint,
            request_timeout=60
        )
        if es_client.ping():
            LOG.info("Elastichsearch aracıyla iletişim başarılı!.")
            return es_client
        else:
            LOG.critical("Elascticsearch aracıyla iletişm başarısız!")
            return None
    except Exception as e:
        LOG.critical(f"Elasticsearch ile bağlantı kurulurken beklenmedik hata: {e}", exc_info=True)
        return None
    
def create_index_if_not_exists(client: Elasticsearch, index_name: str, mapping_body: dict) -> None:
    """
    Açıklama:
        Belirtilen mapping_body ile bir indeks oluşturur. Varsa, işlem yapmaz.
    Args:
        client(Elasticsearch): İndeksin oluşturulacağı hedef Elasticsearch aracının bağlantı nesnesi.
        index_name(str): Oluşturulacak indeksin ismi.
        mapping_body(dict): autocomplete uygulamasının amacına özel yapılandırılmış sözlük.
    """
    LOG.info(f"'{index_name}' indeksi kontrol ediliyor...")
    try:
        if not client.indices.exists(index_name):
            client.indices.create(index=index_name)
            LOG.info(f"{index_name} adında yeni indeks oluşturuldu.")
        else:
            LOG.warning(f"{index_name} adında zaten bir indeks var!")
    except Exception as e:
        LOG.critical(f"{index_name} adında indeks oluşturulurken beklenmedik hata: {e}", exc_info=True)
        raise

