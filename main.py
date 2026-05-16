import os
import uuid
import subprocess
from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from scraper import get_kwai_info, extract_url
import httpx

app = FastAPI(title="dwKwai Downloader")

# Config pastas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

templates = Jinja2Templates(directory="templates")

def cleanup_file(path: str):
    """Remove arquivo temporário."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Erro cleanup: {e}")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/info")
async def info(url: str = Form(...)):
    # url aqui pode vir com texto, get_kwai_info ja trata via extract_url
    data = get_kwai_info(url)
    if not data["success"]:
        return JSONResponse(status_code=400, content=data)
    return data

@app.get("/api/download/mp4")
async def download_mp4(url: str):
    """Proxy para download do MP4 com nome personalizado."""
    try:
        # get_kwai_info ja trata extração de URL internamente
        data = get_kwai_info(url)
        if not data["success"]:
            raise HTTPException(status_code=400, detail="URL inválida")
        
        video_url = data["video_url"]
        filename = f"{data['clean_title']}.mp4"
        
        async def stream_video():
            async with httpx.AsyncClient() as client:
                async with client.stream("GET", video_url, follow_redirects=True) as response:
                    async for chunk in response.aiter_bytes():
                        yield chunk

        return StreamingResponse(
            stream_video(),
            media_type="video/mp4",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/mp3")
async def download_mp3(url: str, background_tasks: BackgroundTasks):
    """Gera MP3 via yt-dlp post-processors e envia."""
    file_id = str(uuid.uuid4())
    temp_file_base = os.path.join(TEMP_DIR, file_id)
    mp3_path = f"{temp_file_base}.mp3"
    
    try:
        # 1. Pegar info (e extrair URL internamente)
        data = get_kwai_info(url, download_audio_only=True)
        if not data["success"]:
            raise HTTPException(status_code=400, detail="URL inválida")
        
        filename = f"{data['clean_title']}.mp3"

        # 2. Download e conversão via yt-dlp (mais eficiente)
        import yt_dlp
        ydl_opts = {
            'outtmpl': temp_file_base,
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([data['source']])
        
        if not os.path.exists(mp3_path):
            raise HTTPException(status_code=500, detail="Falha ao gerar MP3")

        # 3. Agendar cleanup
        background_tasks.add_task(cleanup_file, mp3_path)
        
        return FileResponse(
            mp3_path, 
            media_type="audio/mpeg", 
            filename=filename
        )
        
    except Exception as e:
        cleanup_file(mp3_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
