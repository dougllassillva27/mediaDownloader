"""
Serviço responsável pela interação com o TikTok.
Extrai metadados e links usando yt-dlp com headers otimizados.
"""
import logging
import unicodedata
import re
from scraper import sanitize_filename

logger = logging.getLogger(__name__)

def extract_tiktok_info(url: str):
    """Extrai informações de um vídeo do TikTok."""
    import yt_dlp

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'format': 'best',
        'socket_timeout': 30,
        'retries': 3,
        'ignoreerrors': True,  # Ignora erros de extração parciais
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Sec-Fetch-Mode': 'navigate',
            'Referer': 'https://www.tiktok.com/'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return None, "Não foi possível extrair informações do TikTok."

            title = info.get('title', 'TikTok Video')
            clean_title = sanitize_filename(title)
            video_id = info.get('id', 'unknown')

            return {
                "success": True,
                "title": title,
                "clean_title": clean_title,
                "video_id": video_id,
                "thumbnail": info.get('thumbnail'),
                "source": url
            }, None
    except Exception as e:
        logger.error(f"Erro ao extrair TikTok: {str(e)}")
        return None, f"Erro na extração: {str(e)}"
