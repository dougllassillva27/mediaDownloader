"""
Kwai Downloader - API Principal
Servidor FastAPI para download de vídeos do Kwai com conversão MP3
"""
import os
import uuid
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import yt_dlp
import requests
from scraper import extract_kwai_info, sanitize_filename, clean_text_and_extract_urls

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Diretório temporário
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida da aplicação"""
    yield
    cleanup_temp_files()

app = FastAPI(title="Media Downloader API", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos
if os.path.exists("assets"):
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")

class MediaRequest(BaseModel):
    """Modelo para requisição de mídia"""
    url: str
    format: str = "mp4"  # mp4 ou mp3

class MediaResponse(BaseModel):
    """Modelo para resposta de mídia"""
    success: bool
    download_url: Optional[str] = None
    filename: Optional[str] = None
    message: Optional[str] = None

def cleanup_temp_files():
    """Limpa arquivos temporários antigos"""
    try:
        for filename in os.listdir(TEMP_DIR):
            filepath = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
                logger.info(f"Arquivo temporário removido: {filepath}")
    except Exception as e:
        logger.warning(f"Erro ao limpar arquivos temporários: {e}")

def download_media_file(url: str, format_type: str, temp_filename: str) -> Optional[str]:
    """Baixa o arquivo de mídia (vídeo MP4 ou áudio MP3)"""
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
        'extractor_args': {
            'twitter': {
                'api': 'graphql'
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    # Configurar formato baseado no tipo solicitado
    if format_type == "mp3":
        # Para MP3: baixa apenas o fluxo de áudio (muito mais eficiente)
        ydl_opts['format'] = 'bestaudio'
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        })
        logger.info(f"Extraindo apenas áudio para MP3: {url}")
    else:
        # Para MP4: obtém o melhor vídeo com áudio
        ydl_opts['format'] = 'best[height<=720]'
        logger.info(f"Baixando vídeo MP4: {url}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

            # Procurar arquivo baixado
            base_name = os.path.join(TEMP_DIR, temp_filename)

            if format_type == "mp3":
                # Procurar arquivo MP3
                mp3_file = f"{base_name}.mp3"
                if os.path.exists(mp3_file):
                    return mp3_file

                # Procurar arquivos MP3 com padrão diferente
                for file in os.listdir(TEMP_DIR):
                    if file.startswith(temp_filename) and file.endswith('.mp3'):
                        return os.path.join(TEMP_DIR, file)
            else:
                # Procurar arquivo de vídeo
                video_extensions = ['.mp4', '.webm', '.mkv', '.mov', '.avi']
                for ext in video_extensions:
                    video_file = f"{base_name}{ext}"
                    if os.path.exists(video_file):
                        return video_file

                # Procurar por qualquer arquivo que comece com o nome base
                for file in os.listdir(TEMP_DIR):
                    if file.startswith(temp_filename):
                        return os.path.join(TEMP_DIR, file)

            return None

    except Exception as e:
        logger.error(f"Erro ao baixar mídia: {str(e)}")
        return None

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Página principal"""
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Template não encontrado</h1>"

@app.post("/api/media")
async def get_media_info(request: MediaRequest, background_tasks: BackgroundTasks) -> MediaResponse:
    """Endpoint para obter informações e baixar mídia"""
    try:
        # Extrair URLs do texto fornecido
        urls = clean_text_and_extract_urls(request.url)

        if not urls:
            return MediaResponse(
                success=False,
                message="Nenhuma URL válida do Kwai encontrada no texto fornecido."
            )

        # Usar a primeira URL encontrada
        url = urls[0]

        # Extrair informações
        info = extract_kwai_info(url)

        if not info:
            return MediaResponse(
                success=False,
                message="Não foi possível extrair informações do vídeo. Verifique se a URL está correta."
            )

        # Gerar nome do arquivo
        title = info.get('title', 'video')
        safe_title = sanitize_filename(title)
        unique_id = str(uuid.uuid4())[:8]
        temp_filename = f"{safe_title}_{unique_id}"

        # Baixar arquivo de mídia
        media_file = await asyncio.to_thread(download_media_file, url, request.format, temp_filename)

        if not media_file or not os.path.exists(media_file):
            return MediaResponse(
                success=False,
                message="Erro ao processar o arquivo de mídia."
            )

        # Adicionar tarefa de limpeza
        background_tasks.add_task(cleanup_temp_files)

        # Criar URL de download
        filename = os.path.basename(media_file)
        download_url = f"/download/{filename}"

        return MediaResponse(
            success=True,
            download_url=download_url,
            filename=filename,
            message=f"Arquivo processado com sucesso!"
        )

    except Exception as e:
        logger.error(f"Erro ao processar requisição: {str(e)}")
        return MediaResponse(
            success=False,
            message=f"Erro interno do servidor: {str(e)}"
        )

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Endpoint para download do arquivo processado"""
    filepath = os.path.join(TEMP_DIR, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    # Determinar content-type baseado na extensão
    if filename.endswith('.mp3'):
        media_type = 'audio/mpeg'
    elif filename.endswith('.mp4'):
        media_type = 'video/mp4'
    else:
        media_type = 'application/octet-stream'

    return FileResponse(
        filepath,
        filename=filename,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

@app.get("/api/health")
async def health_check():
    """Endpoint de verificação de saúde"""
    return {"status": "healthy", "service": "Media Downloader API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)