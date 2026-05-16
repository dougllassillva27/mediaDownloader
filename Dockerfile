# Dockerfile para deploy no Render/Vercel (Container)
FROM python:3.11-slim

# Instala FFmpeg e dependências de sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código do projeto
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
