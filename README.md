<div align="center">
  <img src="assets/img/Kwai Downloader Banner.webp" alt="Media Downloader Banner" />
</div>

# Media Downloader

![Status](https://img.shields.io/badge/status-active-success)
![Deploy](https://img.shields.io/badge/deploy-render-46E3B7)
![License](https://img.shields.io/badge/license-MIT-blue)

**Downloader de mídia inteligente, modular e com conversão nativa para MP3.**

Solução robusta para extração de vídeos e áudios com interface profissional, feedback em tempo real e processamento otimizado em servidor.

## 🔗 Demo

Acesse a aplicação em produção:

👉 https://kwaidownloader.dougllassillva.com.br/

## 🌌 Preview

<div align="center">
  <img src="assets/img/Kwai-Downloader.webp" alt="Media Downloader Preview" />
</div>

## 📖 Visão Geral Técnica

O **Media Downloader** é uma aplicação web Full Stack desenvolvida para simplificar a obtenção de mídias. Utiliza uma arquitetura assíncrona baseada em FastAPI para garantir alta performance e escalabilidade.

O sistema integra a poderosa biblioteca `yt-dlp` para extração de metadados e fluxos de mídia, combinada com o `FFmpeg` para conversão de áudio no lado do servidor. A interface é construída em Vanilla JS com um sistema de feedback visual dinâmico (overlays e modais), proporcionando uma experiência de usuário fluida e profissional.

## ⚙️ Highlights técnicos

- **Extração Inteligente:** Detecta URLs de mídia mesmo em meio a blocos de texto usando Regex.
- **Processamento Otimizado:** Download de MP3 baixa apenas o fluxo de áudio, economizando até 80% de banda.
- **Feedback em Tempo Real:** Overlay de loading e modais de sucesso para uma UX sem interrupções.
- **Auto-Cleanup:** Gerenciamento automático de arquivos temporários para manter a saúde do storage.
- **Proxy de Download:** Downloads servidos diretamente pelo backend com nomes de arquivos sanitizados.

## 🏗️ Arquitetura

```txt
Navegador (Frontend Vanilla JS/CSS)
   │
   ▼
FastAPI (Python Backend)
   │
   ├── Scraper (yt-dlp) ───► CDN da plataforma (Extração de metadados)
   ├── Mídia (yt-dlp Post-Processors) ───► Conversão MP3 nativa
   └── Auto-Cleanup (Background Tasks) ───► Remoção de arquivos temp
```

## 📂 Estrutura do projeto

```txt
MediaDownloader/
├── assets/             # Recursos estáticos (Imagens, Ícones)
├── templates/          # Interface HTML e lógica JS
├── temp/               # Diretório para processamento temporário
├── docs/               # Documentação técnica e design
├── Dockerfile          # Definição do ambiente (Python + FFmpeg)
├── main.py             # Entrypoint da API FastAPI
├── scraper.py          # Módulo de scraping e sanitização
└── requirements.txt    # Gerenciamento de dependências
```

## 📂 Responsabilidades

### `main.py`

Entrypoint principal. Gerencia rotas da API, serve arquivos estáticos, orquestra o streaming de vídeo (MP4) e a conversão de áudio (MP3), além de gerenciar tarefas de limpeza em background.

### `scraper.py`

Responsável pela lógica de negócio de extração. Implementa Regex para limpeza de URL, integração com `yt-dlp` para metadados e sanitização de nomes de arquivos para compatibilidade universal.

### `templates/index.html`

Single Page Interface. Contém toda a estrutura visual, estilização Dark Theme e lógica de interação com a API, incluindo gerenciamento de estado da UI (Loading/Modal).

## 🔄 Fluxo principal da aplicação

1. O usuário cola um link (ou texto contendo um link) de mídia.
2. O sistema limpa a URL e extrai metadados (Título, Thumbnail, Duração).
3. A interface exibe um preview rico do vídeo.
4. O usuário seleciona o formato desejado (MP4 ou MP3).
5. O sistema processa a mídia em tempo real com feedback visual (Spinner).
6. O download é disparado e um modal de sucesso é exibido.
7. Arquivos temporários são deletados automaticamente após o envio.

## 🔒 Segurança e privacidade

- **Sanitização de Entrada:** URLs são filtradas rigorosamente via Regex.
- **Nomes de Arquivos Seguros:** Títulos de vídeos são normalizados (remoção de caracteres especiais/acentos).
- **Isolamento Temporário:** Arquivos processados são identificados por UUIDs únicos para evitar colisões.
- **Auto-Destruição:** Arquivos temporários são deletados por Background Tasks do FastAPI imediatamente após o uso.

## 🚀 Como rodar localmente

1. **Pré-requisitos:** Python 3.11+ e FFmpeg instalado no sistema.
2. **Instalação:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Execução:**
   ```bash
   python main.py
   ```
4. **Acesso:** Abra `http://localhost:8000` no seu navegador.

## 📦 Build e Deploy

- **Build:** O projeto utiliza Docker para garantir que o FFmpeg e as dependências Python estejam presentes.
- **Deploy:** Configurado para Render.com, detectando automaticamente o `Dockerfile`.

## 🛠️ Tecnologias

| Tecnologia     | Responsabilidade                     |
| -------------- | ------------------------------------ |
| Python 3.11    | Núcleo do Backend                    |
| FastAPI        | Framework de API de alta performance |
| yt-dlp         | Motor de extração e scraping         |
| FFmpeg         | Processamento e conversão de mídia   |
| Vanilla JS/CSS | Interface leve e responsiva          |
| Docker         | Padronização de ambiente             |

## ✅ Testes

Validações manuais críticas:

- [x] Extração de URL a partir de texto compartilhado.
- [x] Download de MP4 via streaming proxy.
- [x] Conversão de MP3 baixando apenas o fluxo de áudio (Post-processing).
- [x] Exibição e fechamento do modal de sucesso.
- [x] Verificação de deleção de arquivos na pasta `temp/`.

## 📄 Licença

Este projeto está sob a licença MIT.

---

Desenvolvido por **Douglas Silva**.
