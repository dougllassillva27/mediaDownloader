# 🔐 Setup para Download do Instagram

## Por que o Instagram falha?

O Instagram **exige autenticação** mesmo para acessar posts/reels públicos. Sem cookies ou credenciais, o yt-dlp recebe erro:

> "Requested content is not available, rate-limit reached or login required"

## Solução: Exportar Cookies do Navegador

### Passo 1: Instalar Extensão

Instale a extensão **"Get cookies.txt LOCALLY"** no Chrome/Firefox:
- Chrome: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
- Firefox: https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/

### Passo 2: Fazer Login no Instagram

1. Abra uma aba anônima
2. Acesse https://www.instagram.com
3. Faça login com sua conta
4. Mantenha a sessão ativa

### Passo 3: Exportar Cookies

1. Clique na extensão "Get cookies.txt"
2. Clique em **"Download"**
3. Salve o arquivo como `cookies.txt` na raiz do projeto:
   ```
   kwaiDownloader/
   ├── cookies.txt  ← aqui
   ├── main.py
   └── scraper.py
   ```

### Passo 4: Testar

Reinicie o servidor e tente baixar um reel novamente:
```bash
python -m uvicorn main:app --reload --port 8001
```

## ⚠️ Avisos Importantes

- **NUNCA compartilhe seu arquivo `cookies.txt`** — ele contém dados de autenticação da sua conta
- Adicione `cookies.txt` ao `.gitignore` para não enviar acidentalmente ao Git
- Os cookies expiram após alguns dias — reexporte quando necessário
- Use uma conta secundária por segurança

## Alternativa: Usar Arquivo .netrc

Se preferir, configure credenciais via `.netrc`:

1. Crie arquivo `_netrc` (Windows) ou `.netrc` (Linux/Mac):
   ```
   machine instagram.com
   login SEU_USUARIO
   password SUA_SENHA
   ```

2. Proteja o arquivo:
   ```bash
   # Linux/Mac
   chmod 600 ~/.netrc
   
   # Windows (PowerShell)
   icacls $env:USERPROFILE\.netrc /inheritance:r /grant:r %USERNAME%:R
   ```

## Status Atual

✅ **Kwai** — Funciona sem autenticação  
✅ **TikTok** — Funciona sem autenticação  
⚠️ **Instagram** — Requer cookies ou credenciais
