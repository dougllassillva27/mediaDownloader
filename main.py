import logging
import os
import uuid
from contextlib import asynccontextmanager

import httpx
import yt_dlp
from fastapi import BackgroundTasks, FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool

from scraper import detect_platform, get_video_info, is_supported_url, sanitize_filename

# Configurações globais
CHUNK_SIZE_64K = 65536
logger = logging.getLogger(__name__)

class AppState:
    client: httpx.AsyncClient = None

state = AppState()

@asynccontextmanager
async def lifespan(app: FastAPI):
    state.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
    yield
    await state.client.aclose()

app = FastAPI(title="Multi-Platform Downloader (Kwai, TikTok, Instagram)", lifespan=lifespan)

# Config pastas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(TEMP_DIR, exist_ok=True)

app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
templates = Jinja2Templates(directory="templates")

def cleanup_file(path: str):
    """Remove arquivo temporário."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        logger.error(f"Erro cleanup: {e}")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/info")
async def info(url: str = Form(...)):
    try:
        # Verificar se é plataforma suportada
        extracted_url = url.strip()
        if not is_supported_url(extracted_url):
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Plataforma não suportada. Use Kwai, TikTok ou Instagram."}
            )

        platform = detect_platform(extracted_url)
        logger.info(f"Analisando {platform}: {extracted_url[:60]}...")

        data = await run_in_threadpool(get_video_info, url)
        if not data["success"]:
            error_msg = data.get("error", "Erro desconhecido.")
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": f"Erro ao analisar {platform.capitalize()}: {error_msg}"}
            )
        return data
    except Exception as e:
        logger.error(f"Erro /api/info: {e}")
        return JSONResponse(status_code=500, content={"success": False, "error": "Erro interno no servidor."})

@app.get("/api/download/mp4")
async def download_mp4(url: str, filename: str = None):
    """Proxy para download do MP4 com nome personalizado (Kwai, TikTok, Instagram)."""
    try:
        # Verificar plataforma
        if not is_supported_url(url):
            raise HTTPException(status_code=400, detail="Plataforma não suportada.")

        platform = detect_platform(url)
        logger.info(f"Download MP4 - {platform}: {url[:50]}...")

        data = await run_in_threadpool(get_video_info, url)
        if not data["success"]:
            raise HTTPException(status_code=400, detail="URL inválida ou expirada.")

        video_url = data["video_url"]
        final_filename = sanitize_filename(filename) if filename else data["clean_title"]

        async def stream_video():
            async with state.client.stream("GET", video_url) as response:
                if response.status_code != 200:
                    logger.error(f"Erro stream {platform.capitalize()}: Status {response.status_code}")
                    return
                async for chunk in response.aiter_bytes(chunk_size=CHUNK_SIZE_64K):
                    yield chunk

        return StreamingResponse(
            stream_video(),
            media_type="video/mp4",
            headers={"Content-Disposition": f'attachment; filename="{final_filename}.mp4"'}
        )
    except Exception as e:
        logger.error(f"Erro download_mp4: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar download do vídeo.")

@app.get("/api/download/mp3")
async def download_mp3(url: str, background_tasks: BackgroundTasks, filename: str = None):
    """Gera MP3 via yt-dlp post-processors e envia (Kwai, TikTok, Instagram)."""
    file_id = str(uuid.uuid4())
    temp_file_base = os.path.join(TEMP_DIR, file_id)
    mp3_path = f"{temp_file_base}.mp3"

    try:
        # Verificar plataforma
        if not is_supported_url(url):
            raise HTTPException(status_code=400, detail="Plataforma não suportada.")

        platform = detect_platform(url)
        logger.info(f"Download MP3 - {platform}: {url[:50]}...")

        data = await run_in_threadpool(get_video_info, url, True)
        if not data["success"]:
            raise HTTPException(status_code=400, detail="URL inválida ou expirada.")

        final_filename = sanitize_filename(filename) if filename else data["clean_title"]

        ydl_opts = {
            'outtmpl': temp_file_base,
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'socket_timeout': 30,
            'retries': 5,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        # Configurações específicas por plataforma
        if platform == 'tiktok':
            ydl_opts['extractor_args'] = {
                'tiktok': {
                    'api_hostname': 'api22-normal-c-alisg.tiktokv.com',
                    'force_h265': 'False'
                }
            }
        elif platform == 'instagram':
            ydl_opts['extractor_args'] = {
                'instagram': {
                    'api_version': 'v1'
                }
            }

        def _download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([data['source']])

        await run_in_threadpool(_download)

        if not os.path.exists(mp3_path):
            raise HTTPException(status_code=500, detail="Ocorreu um erro na conversão do áudio.")

        background_tasks.add_task(cleanup_file, mp3_path)

        return FileResponse(
            mp3_path,
            media_type="audio/mpeg",
            filename=f"{final_filename}.mp3"
        )

    except Exception as e:
        logger.error(f"Erro download_mp3: {e}")
        cleanup_file(mp3_path)
        raise HTTPException(status_code=500, detail="Erro interno ao converter para MP3.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
