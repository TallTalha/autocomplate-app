# autocomplete-app/api/models/response_models.py
"""API yanıtları için Pydantic veri modellerini tanımlar."""

from pydantic import BaseModel
from typing import List

class SuggestionItem(BaseModel):
    title: str
    category: str
    brand: str

class SuggestionResponse(BaseModel):
    query: str
    suggestions: List[SuggestionItem]