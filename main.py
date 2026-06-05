"""
Endpoint para receber cookies do navegador após login
"""
@app.post("/api/instagram/cookies")
async def receive_instagram_cookies(request: Request):
    """Recebe cookies do Instagram do navegador do usuário e salva em cookies.txt"""
    try:
        data = await request.json()
        cookies = data.get('cookies', [])

        if not cookies:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Nenhum cookie recebido."}
            )

        # Formatar cookies para formato Netscape (cookies.txt)
        cookies_content = []
        cookies_content.append("# Netscape HTTP Cookie File")
        cookies_content.append("# https://curl.haxx.se/docs/http-cookies.html")

        for cookie in cookies:
            # Formato: domain flag path secure expiry name value
            domain = cookie.get('domain', '.instagram.com')
            path = cookie.get('path', '/')
            secure = cookie.get('secure', True)
            expiry = int(cookie.get('expirationDate', time.time() + 86400 * 365))
            name = cookie['name']
            value = cookie['value']

            line = f"{domain}\tTRUE\t{path}\t{str(secure).upper()}\t{expiry}\t{name}\t{value}"
            cookies_content.append(line)

        # Salvar em cookies.txt
        cookies_file = os.path.join(os.path.dirname(__file__), "cookies.txt")
        with open(cookies_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cookies_content))

        logger.info(f"Cookies do Instagram salvos em {cookies_file}")

        return JSONResponse(
            status_code=200,
            content={"success": True, "message": "Cookies salvos com sucesso!"}
        )

    except Exception as e:
        logger.error(f"Erro ao salvar cookies: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )