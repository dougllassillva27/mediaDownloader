"""
Serviço responsável por baixar mídias do Kwai usando yt-dlp.
"""
import os
import asyncio
import logging
import yt_dlp
from .kwai_service import sanitize_filename

logger = logging.getLogger(__name__)

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

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
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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

            # Procura pelo arquivo gerado
            if format_type == "mp3":
                for file in os.listdir(TEMP_DIR):
                    if file.startswith(temp_filename) and file.endswith('.mp3'):
                        return os.path.join(TEMP_DIR, file)
            else:
                video_extensions = ['.mp4', '.webm', '.mkv']
                for ext in video_extensions:
                    video_file = f"{base_name}{ext}"
                    if os.path.exists(video_file):
                        return video_file
                for file in os.listdir(TEMP_DIR):
                    if file.startswith(temp_filename):
                        return os.path.join(TEMP_DIR, file)
            return None
    except Exception as e:
        logger.error(f"Erro no yt-dlp: {str(e)}")
        return None

async def download_media_async(url: str, format_type: str, filename: str) -> dict:
    """Wrapper assíncrono para o download."""
    unique_id = filename.split('_')[-1] if '_' in filename else "tmp"
    safe_name = "_".join(filename.split('_')[:-1]) if '_' in filename else filename

    media_file = await asyncio.to_thread(_download_media, url, format_type, filename)

    if not media_file:
        raise Exception("Falha ao baixar o arquivo de mídia.")

    return {
        "path": media_file,
        "filename": os.path.basename(media_file)
    }
