import yt_dlp
import logging
import re
import unicodedata

# Config log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_url(text: str) -> str:
    """Extrai link do Kwai de um texto usando Regex."""
    pattern = r'(https?://[^\s]+kwai\.com/[^\s]+)'
    match = re.search(pattern, text)
    return match.group(0) if match else text

def sanitize_filename(filename: str) -> str:
    """Limpa nome do arquivo: letras, números e espaços (Opção 1)."""
    # Remove acentos
    nksf = unicodedata.normalize('NFKD', filename)
    filename = "".join([c for c in nksf if not unicodedata.combining(c)])
    # Remove caracteres especiais, mantendo letras, números e espaços
    filename = re.sub(r'[^a-zA-Z0-9\s]', '', filename)
    # Remove espaços extras
    filename = " ".join(filename.split())
    return filename or "kwai_video"

def get_kwai_info(url_input: str, download_audio_only: bool = False):
    """
    Extrai metadados do vídeo Kwai usando yt-dlp.
    """
    url = extract_url(url_input)
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio/best' if download_audio_only else 'bestvideo+bestaudio/best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Kwai Video')
            
            return {
                "success": True,
                "title": title,
                "clean_title": sanitize_filename(title),
                "thumbnail": info.get('thumbnail'),
                "video_url": info.get('url'),
                "duration": info.get('duration'),
                "source": url
            }
    except Exception as e:
        logger.error(f"Erro ao extrair {url}: {e}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Teste rápido
    test_url = "https://k.kwai.com/p/qzeySRCm"
    print(get_kwai_info(test_url))
