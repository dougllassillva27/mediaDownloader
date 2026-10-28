"""
Rotas da API (FastAPI).
Organiza os endpoints e chama os serviços.
"""
import os
import uuid
import asyncio
import logging
from fastapi import APIRouter, Request, BackgroundTasks, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional

from scraper import clean_text_and_extract_urls, sanitize_filename
from services.kwai_service import get_video_metadata
from services.tiktok_service import extract_tiktok_info
from services.download_service import download_media_async
from services.converter_service import convert_to_mp3
from services.url_service import plataforma_da_url, validar_url_plataforma

logger = logging.getLogger(__name__)

router = APIRouter()

class MediaRequest(BaseModel):
    url: str
    format: str = "mp4"

class ConvertResponse(BaseModel):
    success: bool
    download_url: Optional[str] = None
    original_filename: Optional[str] = None
    message: Optional[str] = None

TEMP_DIR = "temp"

# Limite do upload do conversor, aplicado durante a leitura (não depois)
LIMITE_UPLOAD_BYTES = 200 * 1024 * 1024
TAMANHO_CHUNK = 1024 * 1024

@router.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content)
    except FileNotFoundError:
        return HTMLResponse("<h1>Template não encontrado</h1>", status_code=404)

@router.post("/api/info")
async def get_video_info(request: Request):
    from fastapi.responses import JSONResponse
    form = await request.form()
    valor_url = form.get("url", "")
    raw_text = valor_url if isinstance(valor_url, str) else ""

    logger.info(f"Recebido no /api/info: {raw_text}")

    urls = clean_text_and_extract_urls(raw_text)
    logger.info(f"URLs extraídas: {urls}")

    if not urls:
        return JSONResponse({"success": False, "error": "Nenhuma URL válida encontrada."})

    url = urls[0]
    logger.info(f"Tentando processar URL: {url}")

    try:
        validar_url_plataforma(url)
    except ValueError as erro:
        logger.warning(f"URL recusada no /api/info: {erro}")
        return JSONResponse({"success": False, "error": str(erro)})

    # Roteamento inteligente
    try:
        if plataforma_da_url(url) == "tiktok.com":
            logger.info("Detectado como TikTok")
            data, error = extract_tiktok_info(url)
        else:
            logger.info("Detectado como Kwai")
            data, error = get_video_metadata(url)
    except Exception as e:
        logger.error(f"Erro no roteamento: {e}")
        return JSONResponse({"success": False, "error": f"Erro interno: {str(e)}"})

    if error or not data:
        return JSONResponse({"success": False, "error": error or "Erro ao extrair informações."})

    return JSONResponse(data)

@router.get("/api/download/mp4")
async def download_mp4(url: str, filename: str = None, background_tasks: BackgroundTasks = None):
    try:
        validar_url_plataforma(url)
        result = await download_media_async(url, "mp4", filename or "video")
        path = result["path"]

        if not os.path.exists(path):
            raise Exception(f"Arquivo não encontrado no caminho: {path}")

        logger.info(f"Servindo arquivo MP4: {path} ({os.path.getsize(path)} bytes)")

        if background_tasks:
            background_tasks.add_task(lambda p=path: os.remove(p) if os.path.exists(p) else None)

        return FileResponse(path, filename=result["filename"], media_type="video/mp4")
    except ValueError as e:
        logger.warning(f"URL recusada no MP4: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro MP4: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/download/mp3")
async def download_mp3(url: str, filename: str = None, background_tasks: BackgroundTasks = None):
    try:
        validar_url_plataforma(url)
        result = await download_media_async(url, "mp3", filename or "audio")
        path = result["path"]

        if not os.path.exists(path):
            raise Exception(f"Arquivo não encontrado no caminho: {path}")

        logger.info(f"Servindo arquivo MP3: {path} ({os.path.getsize(path)} bytes)")

        if background_tasks:
            background_tasks.add_task(lambda p=path: os.remove(p) if os.path.exists(p) else None)

        return FileResponse(path, filename=result["filename"], media_type="audio/mpeg")
    except ValueError as e:
        logger.warning(f"URL recusada no MP3: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro MP3: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/convert")
async def convert_video(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    allowed_extensions = {'.mp4', '.ts', '.mkv', '.avi', '.mov', '.webm'}
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Formato não suportado. Use: {', '.join(sorted(allowed_extensions))}")

    conteudo = bytearray()
    while True:
        pedaco = await file.read(TAMANHO_CHUNK)
        if not pedaco:
            break
        conteudo.extend(pedaco)
        if len(conteudo) > LIMITE_UPLOAD_BYTES:
            raise HTTPException(status_code=400, detail="Arquivo muito grande. Limite: 200MB")

    content = bytes(conteudo)

    unique_id = str(uuid.uuid4())[:8]
    safe_name = sanitize_filename(os.path.splitext(file.filename)[0])
    input_filename = f"{safe_name}_{unique_id}{file_ext}"
    output_filename = f"{safe_name}_{unique_id}.mp3"

    input_path = os.path.join(TEMP_DIR, input_filename)
    output_path = os.path.join(TEMP_DIR, output_filename)

    with open(input_path, 'wb') as f:
        f.write(content)

    success = await asyncio.to_thread(convert_to_mp3, input_path, output_path)

    if os.path.exists(input_path):
        os.remove(input_path)

    if not success:
        raise HTTPException(status_code=500, detail="Erro na conversão.")

    # Serve o arquivo convertido diretamente
    if not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail="Arquivo de saída não encontrado após conversão.")

    return FileResponse(
        output_path,
        filename=output_filename,
        media_type="audio/mpeg",
        background=background_tasks
    )
