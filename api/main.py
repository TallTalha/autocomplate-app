# autocomplete-app/api/main.py
"""Autocomplete API'sinin giriş noktası (entry point)."""

import logging
import os
import sys
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from fastapi import FastAPI
from elasticsearch import Elasticsearch

from .services import es_search_service
from .models.response_models import SuggestionResponse
from .configs.api_configs import ES_URL, ES_USER, ES_PASS, ES_FINGER, ES_INDEX

app_dir = os.path.dirname(os.path.abspath(__file__)) # /autocomplete-app/api
project_dir = os.path.dirname(app_dir) # /autocomplete-app
sys.path.append(project_dir)

# LOG
from utils.logger import setup_logger
setup_logger(name="api_main", app_dir=app_dir)

# FastApi Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başladığında Elasticsearch istemcisini oluşturur."""
    LOG = logging.getLogger(__name__)
    LOG.info("API başlatılıyor: Elasticsearch istemcisi oluşturuluyor...")
    try:
        client = Elasticsearch(
            hosts=[ES_URL],
            basic_auth=(ES_USER, ES_PASS),
            ssl_assert_fingerprint=ES_FINGER,
            request_timeout=10
        )

        if not client.ping():
            LOG.error("Elasticsearch ping başarısız. Küme ayakta ama cevap vermiyor.")
            es_search_service.es_client = None
        else:
            LOG.info("Elasticsearch istemcisi başarıyla oluşturuldu ve bağlandı.")
            es_search_service.es_client = client

    except Exception as e:
        LOG.critical(f"Elastich Search bağlnatısı sırasında beklenmedik hata: {e}", exc_info=True)
        es_search_service.es_client = None

    yield

    LOG.info("API kapatılıyor...")

    # uygulama kapandığında çalışır (örn: Ctrl+C)
    LOG.info("API kapatılıyor...")
    # Elasticsearch istemcisinin kapatılmasına gerek yoktur,
    # bağlantı havuzunu kendi yönetir.


app = FastAPI(lifespan=lifespan, title="Autocomplete API")
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Tüm metotlara (GET, POST vb.) izin ver
    allow_headers=["*"], # Tüm başlıklara izin ver
)

LOG = logging.getLogger(__name__)



# --- API Endpoint'i ---
@app.get("/search", response_model=SuggestionResponse)
async def get_suggestions(term: str) -> Dict[str, List]:
    """
    Açıklama:
        Verilen bir 'term' (arama metni) için autocomplete önerileri döndürür.
    Args:
        term(str): Frontend'den gelen arama metni.
    Returns:
        result(Dict[str, List]): {"query": term, "suggestions": suggestions_list} yapısındaki autocomplete önerileri döner.
    """
    LOG.info(f"Arama isteği alındı: term='{term}'")

    if not es_search_service.es_client:
        return {"query": term, "suggestions": []}
    
    suggestions_list = es_search_service.fetch_auto_complete_suggestions( index_name=ES_INDEX, query_text=term)
    result = {"query": term, "suggestions": suggestions_list} 
    
    return result