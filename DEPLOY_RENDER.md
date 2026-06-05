# 🚀 Deploy no Render.com - Kwai Downloader

## Configuração Inicial

### 1. Criar Web Service no Render

1. Acesse https://render.com e faça login
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório GitHub
4. Configure:
   - **Name:** `kwai-downloader`
   - **Branch:** `main`
   - **Root Directory:** `/` (raiz do repo)
   - **Runtime:** `Docker`
   - **Instance Type:** Free (ou Basic $7/mês para mais performance)

### 2. Variáveis de Ambiente

No dashboard do serviço, vá em **"Environment"** e adicione:

```
RENDER=true
```

### 3. Arquivo de Cookies (Opcional - Para Instagram)

Se quiser suporte a Instagram em produção:

1. Exporte cookies do seu navegador (veja `INSTAGRAM_SETUP.md`)
2. No dashboard Render, vá em **"Environment"** → **"Environment Files"**
3. Adicione um novo arquivo:
   - **Path:** `/app/cookies.txt`
   - **Content:** Cole o conteúdo do arquivo `cookies.txt`

⚠️ **Atenção:** Cookies expiram em 7-14 dias. Você precisará atualizar periodicamente.

### 4. Deploy

Clique em **"Create Web Service"**. O Render vai:
1. Clonar seu repo
2. Build da imagem Docker
3. Deploy automático

URL final: `https://kwai-downloader.onrender.com`

## Estrutura do Dockerfile

O `Dockerfile` já está configurado para:
- ✅ Instalar Python 3.11 + FFmpeg
- ✅ Copiar código do projeto
- ✅ Instalar dependências do `requirements.txt`
- ✅ Expor porta 8000
- ✅ Suportar variável `RENDER=true`

## Limitações do Render Free Tier

- ⏱️ **Spin down após 15 min de inatividade** (primeiro acesso leva ~30s)
- 💾 **750 horas/mês gratuitas** (~31 dias contínuos)
- 📦 **Sem persistência de disco** (arquivos `temp/` são perdidos no redeploy)
- 🌐 **Sem fallback local para MP3** (container stateless)

## Monitoramento

- Logs: Dashboard → **"Logs"** (stream em tempo real)
- Métricas: CPU, memória, uso de disco
- Health check: `GET /api/health`

## Atualização de Cookies

Quando os cookies expirarem:

1. Reexporte do navegador
2. No Render dashboard: **Environment** → **Environment Files** → Edite `/app/cookies.txt`
3. Redeploy automático (ou manual: **"Manual Deploy"** → **"Clear build cache & deploy"**)

## Custo Estimado

- **Free tier:** $0 (limitações acima)
- **Basic tier:** $7/mês (sem spin down, mais recursos)
- **Standard tier:** $25/mês (produção robusta)

## Troubleshooting

### Erro: "Instagram rate-limit"
- Solução: Atualize cookies.txt ou aguarde 30 min

### Erro: "ModuleNotFoundError"
- Solução: Verifique se `requirements.txt` está completo na raiz

### Deploy falha
- Solução: Veja logs em **"Events"** no dashboard

## URL Personalizada

Para usar domínio próprio:
1. Vá em **"Settings"** → **"Custom Domain"**
2. Adicione seu domínio (ex: `kwaidownloader.dougllassillva.com.br`)
3. Configure DNS CNAME conforme instruções do Render
