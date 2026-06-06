"""
Serviço responsável pela interação com o Kwai.
Extrai metadados e limpa URLs.
"""
import re
import logging
import unicodedata
from scraper import extract_kwai_info, sanitize_filename, clean_text_and_extract_urls

logger = logging.getLogger(__name__)

def get_video_metadata(raw_text: str):
    """Extrai metadados de um texto bruto contendo uma URL do Kwai."""
    urls = clean_text_and_extract_urls(raw_text)
    if not urls:
        return None, "Nenhuma URL válida encontrada."

    url = urls[0]
    info = extract_kwai_info(url)

    if not info:
        return None, "Não foi possível extrair informações do vídeo."

    title = info.get('title', 'Kwai Video')
    clean_title = sanitize_filename(title)

    return {
        "success": True,
        "title": title,
        "clean_title": clean_title,
        "thumbnail": info.get('thumbnail'),
        "source": url
    }, None
