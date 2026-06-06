"""
Serviço responsável por converter arquivos locais para MP3.
"""
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

TEMP_DIR = "temp"

def convert_to_mp3(input_path: str, output_path: str) -> bool:
    """Converte arquivo de vídeo para MP3 usando ffmpeg."""
    try:
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-vn',
            '-acodec', 'libmp3lame',
            '-ac', '2',
            '-b:a', '192k',
            '-ar', '44100',
            '-f', 'mp3',
            '-y',
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1024:
            return True
        else:
            logger.error(f"Falha na conversão. stderr: {result.stderr}")
            return False
    except FileNotFoundError:
        logger.error("ERRO CRÍTICO: 'ffmpeg' não encontrado no PATH.")
        return False
    except Exception as e:
        logger.error(f"Erro ao converter: {str(e)}")
        return False
