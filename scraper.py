"""
Scraper de Mídia - Media Downloader
Módulo responsável por extrair informações de vídeos do Kwai usando yt-dlp.
"""
import yt_dlp
import re
import logging
from typing import Optional, Dict, Any

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_kwai_info(url: str) -> Optional[Dict[str, Any]]:
    """Extrai informações de um vídeo do Kwai"""
    if not url or 'kwai.com' not in url:
        return None

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'format': 'best',
        'socket_timeout': 10,
        'retries': 3,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info and 'entries' in info and len(info['entries']) > 0:
                info = info['entries'][0]
            return info
    except Exception as e:
        logger.error(f"Erro ao extrair informações do Kwai: {str(e)}")
        return None

def sanitize_filename(title: str) -> str:
    """Sanitiza o título para criar nomes de arquivos válidos"""
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title)
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = ''.join(c for c in sanitized if c.isascii())
    sanitized = unicodedata.normalize('NFKD', sanitized).encode('ascii', 'ignore').decode('ascii')
    sanitized = sanitized.strip('_').strip('.')
    if not sanitized:
        sanitized = "video"
    return sanitized[:100]

def is_valid_kwai_url(url: str) -> bool:
    """Verifica se é uma URL válida do Kwai"""
    kwai_pattern = r'(?:https?://(?:www\.)?(?:kwai\.com/)|@?(?:[a-zA-Z0-9_-]+)\.kwai\.com/)'
    return bool(re.search(kwai_pattern, url))

def clean_text_and_extract_urls(text: str) -> list:
    """Limpa o texto e extrai URLs do Kwai"""
    if not text:
        return []

    url_pattern = r'https?://[^\s<>"]*kwai\.com/[^\s<>"]*'
    urls = re.findall(url_pattern, text)
    return urls if urls else []