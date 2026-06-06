"""
Ponto de entrada principal da aplicação.
Inicializa o servidor FastAPI e inclui as rotas.
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router as api_router

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Diretório temporário
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

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

# Incluir rotas da API
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8200))
    uvicorn.run(app, host="127.0.0.1", port=port)
