# Design do Projeto: dwKwai Downloader

Este documento detalha a arquitetura e as decisões técnicas para o site de download de vídeos do Kwai.

## 🏗️ Arquitetura do Sistema

O sistema é dividido em duas partes principais:

1.  **Backend (Python/FastAPI):**
    - Responsável pelo scraping da URL do Kwai.
    - Processamento de mídia usando FFmpeg.
    - Serviço de streaming para entrega dos arquivos.
2.  **Frontend (Vanilla JS/CSS ou React):**
    - Interface limpa com campo de entrada de URL.
    - Exibição de preview (Thumbnail e Título).
    - Botões de ação para MP4 e MP3.

## 🛠️ Stack Tecnológica

- **Linguagem:** Python 3.9+
- **Framework Web:** FastAPI (pela performance e documentação automática).
- **Extração de Dados:** `httpx` + `BeautifulSoup4` ou `yt-dlp` (para scraping robusto).
- **Processamento de Áudio:** `FFmpeg` (via subprocess ou wrapper python).
- **Hospedagem Recomendada:** Render.com (suporte nativo a Docker/FFmpeg).

## 🔄 Fluxo de Dados

1.  **Input:** Usuário cola o link `https://k.kwai.com/p/...`
2.  **Scraping:** O servidor acessa a URL, segue os redirecionamentos e encontra a URL direta do vídeo (.mp4) e a imagem de capa.
3.  **Preview:** O servidor retorna os metadados para o frontend exibir a miniatura.
4.  **Download MP4:** O servidor faz um túnel (proxy) da URL do CDN do Kwai para o usuário.
5.  **Download MP3:**
    - Servidor baixa o MP4 para uma pasta `/temp`.
    - FFmpeg extrai o áudio em formato MP3.
    - Servidor envia o MP3 para o usuário.
    - **Auto-Cleanup:** O arquivo é deletado imediatamente após o envio.

## 📋 Registro de Decisões (Decision Log)

- **Decisão:** Scraping Direto vs API.
  - **Escolha:** Scraping Direto.
  - **Motivo:** Independência de serviços de terceiros e controle total da lógica.
- **Decisão:** Conversão de Áudio.
  - **Escolha:** FFmpeg no Servidor.
  - **Motivo:** Garante que qualquer vídeo possa ser convertido para áudio de alta qualidade.
- **Decisão:** Plataforma de Deploy.
  - **Escolha:** Render.
  - **Motivo:** Facilidade em instalar dependências de sistema como FFmpeg comparado a Vercel/Netlify.

## 🚀 Estratégia de Deploy

Será utilizado um `Dockerfile` ou as instruções de `render.yaml` para garantir que o binário do FFmpeg esteja disponível no ambiente de execução.
