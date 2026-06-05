"""
Teste exploratório para validar yt-dlp com TikTok e Instagram
"""
import yt_dlp


def test_platform(url: str, platform: str):
    """Testa extração de metadados para uma URL"""
    print(f"\n{'='*60}")
    print(f"Plataforma: {platform}")
    print(f"URL: {url}")
    print('='*60)

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'format': 'best',
        'socket_timeout': 10,
        'retries': 3,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info and 'entries' in info and len(info['entries']) > 0:
                info = info['entries'][0]

            print(f"✅ Título: {info.get('title', 'N/A')}")
            print(f"📺 Thumbnail: {info.get('thumbnail', 'N/A')[:80]}...")
            print(f"⏱ Duração: {info.get('duration', 'N/A')}s")
            print(f"🔑 Extractor: {info.get('extractor_key', 'N/A')}")
            print(f"📡 Formato: {info.get('format', 'N/A')}")
            return True
    except Exception as e:
        print(f"❌ Erro: {str(e)[:200]}")
        return False

if __name__ == "__main__":
    # URLs de teste (substituir por URLs reais ao executar)
    test_cases = [
        ("https://www.kwai.com/@username/video/123456", "Kwai"),
        ("https://www.tiktok.com/@username/video/1234567890", "TikTok"),
        ("https://vm.tiktok.com/ZMhKjExample/", "TikTok Short"),
        ("https://www.instagram.com/p/ABC123Example/", "Instagram Post"),
        ("https://www.instagram.com/reel/XYZ789Example/", "Instagram Reel"),
    ]

    results = []
    for url, platform in test_cases:
        success = test_platform(url, platform)
        results.append((platform, success))

    print(f"\n{'='*60}")
    print("RESUMO:")
    for platform, success in results:
        status = "✅ OK" if success else "❌ FALHOU"
        print(f"  {platform}: {status}")
