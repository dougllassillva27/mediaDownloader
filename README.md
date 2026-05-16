# Kwai Downloader

![Status](https://img.shields.io/badge/status-active-success)
![Deploy](https://img.shields.io/badge/deploy-render-46E3B7)
![License](https://img.shields.io/badge/license-MIT-blue)

**Downloader de Kwai inteligente, modular e com conversão nativa para MP3.**

Solução robusta para extração de vídeos e áudios do Kwai com interface profissional e processamento em servidor.

## 🔗 Demo

> Deploy recomendado em Render.com para suporte nativo a FFmpeg.

## 🌌 Preview

*(Preview indisponível no momento)*

## ⚙️ Highlights técnicos

- Extração direta via Scraping (yt-dlp)
- Processamento de áudio via FFmpeg no servidor
- Interface moderna com visualização de miniatura (Preview UX)
- Sistema de Auto-Cleanup para economia de storage
- Backend assíncrono com FastAPI

## 🏗️ Arquitetura

```txt
Navegador (Frontend Vanilla JS/CSS)
   │
   ▼
FastAPI (Python Backend)
   │
   ├── Scraper (yt-dlp) ───► Kwai CDN
   ├── Mídia (FFmpeg)   ───► MP3 Engine
   └── Auto-Cleanup     ───► Temp Files
```

## 📂 Estrutura do projeto

```txt
KwaiDownloader/
├── templates/          # Interface HTML/JS
├── temp/               # Arquivos temporários (auto-deleted)
├── docs/               # Documentação técnica
├── Dockerfile          # Configuração de container (FFmpeg)
├── main.py             # Servidor FastAPI
├── scraper.py          # Lógica de extração
└── requirements.txt    # Dependências Python
```

## 🛠️ Tecnologias

| Tecnologia | Responsabilidade |
| --- | --- |
| Python 3.11 | Linguagem base |
| FastAPI | Framework Web/API |
| yt-dlp | Scraping e Extração |
| FFmpeg | Conversão MP4 -> MP3 |
| Docker | Padronização de Ambiente |

## 🔄 Fluxo principal da aplicação

1. Usuário insere link do Kwai.
2. Backend extrai metadados (Título e Thumbnail).
3. Frontend exibe o Preview para confirmação.
4. Usuário escolhe MP4 (link direto) ou MP3 (processamento).
5. No MP3, o servidor baixa, converte e entrega o arquivo.
6. O sistema deleta os arquivos temporários imediatamente.

## 🚀 Como rodar localmente

1. Certifique-se de ter o Python 3.11 e FFmpeg instalados.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o servidor:
   ```bash
   python main.py
   ```
4. Acesse `http://localhost:8000`.

## 📦 Deploy (Render.com)

1. Conecte o repositório ao Render.
2. Escolha **Web Service**.
3. O Render detectará o `Dockerfile` automaticamente.
4. O FFmpeg será instalado durante o build do container.

## 📄 Licença

Este projeto está sob a licença MIT.

---
Desenvolvido por Douglas Silva.
