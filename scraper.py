import logging
import os
import re
import unicodedata

import yt_dlp

# Config log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho para arquivo de cookies (opcional, para Instagram)
COOKIES_FILE = os.path.join(os.path.dirname(__file__), "cookies.txt")

def detect_platform(url: str) -> str:
    """Detecta plataforma baseada na URL."""
    if 'tiktok.com' in url or 'vm.tiktok.com' in url:
        return 'tiktok'
    elif 'instagram.com' in url:
        return 'instagram'
    elif 'kwai.com' in url:
        return 'kwai'
    return 'unknown'

def extract_url(text: str) -> str:
    """Extrai primeira URL válida de um texto."""
    pattern = r'(https?://[^\s<>"\']+)'
    match = re.search(pattern, text)
    return match.group(0) if match else text

def is_supported_url(url: str) -> bool:
    """Verifica se URL é de plataforma suportada."""
    platform = detect_platform(url)
    return platform in ['kwai', 'tiktok', 'instagram']

MAX_FILENAME_LENGTH = 80
CACHE_SIZE = 128

def sanitize_filename(filename: str) -> str:
    """
    Limpa nome do arquivo para garantir compatibilidade com SOs.
    Decompõe acentos, remove caracteres especiais e limita o tamanho.
    """
    if not filename:
        return "video"

    # Normaliza texto (NFKD decompõe caracteres como 'á' em 'a' + '´')
    normalized_text = unicodedata.normalize('NFKD', filename)
    filename = "".join([c for c in normalized_text if not unicodedata.combining(c)])

    # Remove caracteres especiais, mantendo letras, números, espaços, hifens e underscores
    filename = re.sub(r'[^a-zA-Z0-9\s\-_]', '', filename)

    # Remove espaços extras e substitui por espaço simples
    filename = " ".join(filename.split())

    # Trunca para evitar limite do Windows (260 chars caminho completo)
    max_len = min(MAX_FILENAME_LENGTH, 80)
    filename = filename[:max_len]

    return filename.strip() or "video"

def get_video_info(url_input: str, download_audio_only: bool = False):
    """
    Dispatcher genérico: detecta plataforma e extrai metadados.
    Suporta Kwai, TikTok e Instagram.
    """
    url = extract_url(url_input)
    platform = detect_platform(url)

    if platform == 'unknown':
        return {
            "success": False,
            "error": "Plataforma não suportada. Use Kwai, TikTok ou Instagram."
        }

    # Configurações específicas por plataforma
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio/best' if download_audio_only else 'bestvideo+bestaudio/best',
        'socket_timeout': 15,
        'retries': 3,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    # Configurações específicas para TikTok
    if platform == 'tiktok':
        ydl_opts['extractor_args'] = {
            'tiktok': {
                'api_hostname': 'api22-normal-c-alisg.tiktokv.com',
                'force_h265': 'False'
            }
        }

    # Configurações específicas para Instagram
    elif platform == 'instagram':
        ydl_opts['extractor_args'] = {
            'instagram': {
                'api_version': 'v1'
            }
        }
        # Usar cookies se disponíveis (necessário para Instagram)
        if os.path.exists(COOKIES_FILE):
            ydl_opts['cookiefile'] = COOKIES_FILE
            logger.info("Usando cookies.txt para autenticação Instagram")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Handle playlist/entries
            if info and 'entries' in info and len(info['entries']) > 0:
                info = info['entries'][0]

            title = info.get('title', f'{platform.capitalize()} Video')

            return {
                "success": True,
                "title": title,
                "clean_title": sanitize_filename(title),
                "thumbnail": info.get('thumbnail'),
                "video_url": info.get('url'),
                "duration": info.get('duration'),
                "source": url,
                "platform": platform
            }
    except Exception as e:
        logger.error(f"Erro ao extrair {url} ({platform}): {e}")
        return {
            "success": False,
            "error": str(e),
            "platform": platform
        }

# Manter compatibilidade com código existente
get_kwai_info = get_video_info

if __name__ == "__main__":
    # Teste rápido
    test_url = "https://k.kwai.com/p/qzeySRCm"
    print(get_kwai_info(test_url))
