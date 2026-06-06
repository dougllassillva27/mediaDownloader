<div align="center">
  <img src="assets/img/Kwai Downloader Banner.webp" alt="Media Downloader Banner" />
</div>

# Media Downloader

![Status](https://img.shields.io/badge/status-active-success)
![Deploy](https://img.shields.io/badge/deploy-render-46E3B7)
![License](https://img.shields.io/badge/license-MIT-blue)

**Downloader de mídia modular com FastAPI, conversão nativa para MP3 e suporte a Kwai.**

## 🔗 Demo

Acesse a aplicação em produção:

👉 https://mediadownloader.dougllassillva.com.br/

## 🌌 Preview

<div align="center">
  <img src="assets/img/Kwai-Downloader.webp" alt="Media Downloader Preview" />
</div>

## 📖 Visão Geral Técnica

O **Media Downloader** é uma aplicação web Full Stack baseada em FastAPI com frontend Vanilla JS. Arquitetura modular separada em serviços (`services/`), rotas de API (`routes/`) e templates (`templates/`). Processamento assíncrono com `yt-dlp` para extração de mídia e `ffmpeg` para conversão de áudio no servidor.

## ⚙️ Highlights técnicos

- **Extração Inteligente:** Detecta URLs de mídia em blocos de texto via Regex.
- **Download Eficiente:** MP3 baixa apenas fluxo de áudio, economizando banda.
- **Conversor Local:** Suporta .mp4, .ts, .mkv, .avi, .mov, .webm (até 200MB) convertidos para MP3 via ffmpeg.
- **Feedback em Tempo Real:** UI com overlays de loading e modais de sucesso.
- **Auto-Cleanup:** Arquivos temporários removidos após processamento.

## 🏗️ Arquitetura

```
Navegador (Vanilla JS/CSS)
   │
   ▼
FastAPI (Python Backend)
   │
   ├── routes/api.py ───► Endpoints da API
   ├── services/
   │   ├── kwai_service.py      # Extração Kwai
   │   ├── download_service.py  # Download yt-dlp
   │   └── converter_service.py # Conversão local FFmpeg
   └── temp/                    # Arquivos temporários (auto-cleanup)
```

## 📂 Estrutura do projeto

```
mediaDownloader/
├── assets/                 # Recursos estáticos (imagens, ícones)
├── templates/              # Frontend HTML/CSS/JS
├── services/               # Lógica de negócio
│   ├── kwai_service.py
│   ├── download_service.py
│   └── converter_service.py
├── routes/                 # Endpoints da API
│   └── api.py
├── temp/                   # Arquivos temporários de processamento
├── docs/                   # Documentação técnica
├── Dockerfile              # Ambiente Python + FFmpeg
├── main.py                 # Entry point FastAPI
├── scraper.py              # Módulo de scraping legacy
└── requirements.txt        # Dependências
```

## 📂 Responsabilidades

### `main.py`

Entry point FastAPI. Monta rotas da API, serve estáticos e gerencia ciclo de vida (cleanup de `temp/`). Porta padrão: **8200**.

### `services/kwai_service.py`

Extração de metadados e URLs de vídeos do Kwai via `yt-dlp`.

### `services/download_service.py`

Download de mídia (MP4/MP3) com post-processing de áudio.

### `services/converter_service.py`

Conversão local de arquivos de vídeo (.mp4, .ts, .mkv, .avi, .mov, .webm) para MP3 usando ffmpeg. Limite de 200MB.

### `routes/api.py`

Define endpoints REST para extração Kwai, download e conversão.

### `templates/index.html`

Interface single-page com Vanilla JS, estilização dark theme e comunicação com API.

## 🔄 Fluxo principal

1. Usuário cola URL ou texto contendo link de mídia.
2. Sistema extrai URL limpa e busca metadados (título, thumbnail, duração).
3. Preview exibido na interface.
4. Usuário seleciona formato (MP4 ou MP3).
5. Backend processa mídia com feedback visual (spinner).
6. Download disparado e modal de sucesso exibido.
7. Arquivos temporários deletados automaticamente.

## 🔒 Segurança e privacidade

- **Sanitização de Entrada:** URLs filtradas via Regex.
- **Nomes Seguros:** Caracteres especiais e acentos removidos.
- **Isolamento por UUID:** Arquivos temporários identificados unicamente.
- **Auto-Destruição:** Cleanup via Background Tasks do FastAPI.

## 🚀 Como rodar localmente

1. **Pré-requisitos:** Python 3.10+ e FFmpeg instalado no sistema.
2. **Instalação:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Execução:**
   ```bash
   python main.py
   ```
4. **Acesso:** Abra `http://localhost:8200` no navegador.

## ✅ Qualidade e Testes

```bash
ruff check .     # Linting Python
pytest           # Testes unitários
```

## 📦 Deploy no Render

Projeto utiliza `Dockerfile` com suporte nativo a FFmpeg. Deploy configurado no Render.com detectando o Dockerfile automaticamente.

## 🛠️ Tecnologias

| Tecnologia       | Responsabilidade                     |
| ---------------- | ------------------------------------ |
| Python 3.10+     | Núcleo do Backend                    |
| FastAPI          | Framework de API de alta performance |
| yt-dlp           | Motor de extração e scraping         |
| FFmpeg           | Processamento e conversão de mídia   |
| Vanilla JS/CSS   | Interface leve e responsiva          |
| Docker           | Padronização de ambiente             |

## 📄 Licença

Este projeto está sob a licença MIT.

---

Desenvolvido por **Douglas Silva**.
