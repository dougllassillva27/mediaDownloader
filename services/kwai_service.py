"""
Serviço responsável pela interação com o Kwai.
Extrai metadados e limpa URLs.
"""
import logging

from scraper import extract_kwai_info, sanitize_filename

logger = logging.getLogger(__name__)


def get_video_metadata(url: str):
    """Extrai metadados de uma URL do Kwai já validada pela rota."""
    if not url:
        return None, "Nenhuma URL válida encontrada."

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
