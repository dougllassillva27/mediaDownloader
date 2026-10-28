"""
Serviço responsável por baixar mídias do Kwai usando yt-dlp.

O nome do arquivo de saída é gerado aqui (uuid); o nome escolhido pelo usuário é
sanitizado e usado apenas como nome de exibição no download.
"""
import os
import asyncio
import logging
import uuid
import yt_dlp
from .kwai_service import sanitize_filename

logger = logging.getLogger(__name__)

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


def _nome_interno() -> str:
    """Nome de arquivo gerado pelo servidor, sem entrada do usuário."""
    return f"media_{uuid.uuid4().hex[:12]}"


def _dentro_do_temp(caminho: str) -> bool:
    """Confirma que o caminho resolvido permanece dentro de TEMP_DIR."""
    raiz = os.path.realpath(TEMP_DIR)
    alvo = os.path.realpath(caminho)
    return alvo == raiz or alvo.startswith(raiz + os.sep)


def _download_media(url: str, format_type: str, temp_filename: str) -> str:
    """Lógica interna de download (síncrona)."""
    output_path = os.path.join(TEMP_DIR, f"{temp_filename}.%(ext)s")

    ydl_opts = {
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'postprocessors': [],
        'socket_timeout': 30,
        'retries': 5,
        'fragment_retries': 5,
        'ignoreerrors': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.tiktok.com/'
        }
    }

    if format_type == "mp3":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        })
    else:
        ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

            base_name = os.path.join(TEMP_DIR, temp_filename)

            # Procura pelo arquivo gerado, sempre confinado ao TEMP_DIR
            if format_type == "mp3":
                for file in os.listdir(TEMP_DIR):
                    if file.startswith(temp_filename) and file.endswith('.mp3'):
                        candidato = os.path.join(TEMP_DIR, file)
                        if _dentro_do_temp(candidato):
                            return candidato
            else:
                video_extensions = ['.mp4', '.webm', '.mkv']
                for ext in video_extensions:
                    video_file = f"{base_name}{ext}"
                    if os.path.exists(video_file) and _dentro_do_temp(video_file):
                        return video_file
                for file in os.listdir(TEMP_DIR):
                    if file.startswith(temp_filename):
                        candidato = os.path.join(TEMP_DIR, file)
                        if _dentro_do_temp(candidato):
                            return candidato
            return None
    except Exception as e:
        logger.error(f"Erro no yt-dlp: {str(e)}")
        return None


async def download_media_async(url: str, format_type: str, filename: str) -> dict:
    """Wrapper assíncrono para o download."""
    nome_exibicao = sanitize_filename(filename) or ("audio" if format_type == "mp3" else "video")
    media_file = await asyncio.to_thread(_download_media, url, format_type, _nome_interno())

    if not media_file:
        raise Exception("Falha ao baixar o arquivo de mídia.")

    extensao = os.path.splitext(media_file)[1] or (".mp3" if format_type == "mp3" else ".mp4")

    return {
        "path": media_file,
        "filename": f"{nome_exibicao}{extensao}"
    }
