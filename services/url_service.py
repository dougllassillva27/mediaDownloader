"""
Validação de URL das plataformas suportadas.

O check por substring ("kwai.com" in url) aceitava qualquer host que contivesse o
texto. Aqui a comparação é feita no hostname normalizado e o destino resolvido é
conferido para não apontar para rede interna.
"""
import ipaddress
import socket
from urllib.parse import urlsplit
from typing import Optional

PLATAFORMAS = ("kwai.com", "tiktok.com")


def plataforma_da_url(url: Optional[str]) -> Optional[str]:
    """Devolve o domínio da plataforma quando o hostname pertence a ele."""
    if not url:
        return None
    host = (urlsplit(url).hostname or "").lower().rstrip(".")
    if not host:
        return None
    for dominio in PLATAFORMAS:
        if host == dominio or host.endswith("." + dominio):
            return dominio
    return None


def _enderecos_publicos(host: str, porta: int) -> bool:
    """Confirma que todos os endereços resolvidos são públicos."""
    try:
        infos = socket.getaddrinfo(host, porta, proto=socket.IPPROTO_TCP)
    except OSError:
        return False

    for info in infos:
        endereco = info[4][0]
        try:
            ip = ipaddress.ip_address(endereco)
        except ValueError:
            return False
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        ):
            return False
    return True


def validar_url_plataforma(url: str) -> str:
    """Valida esquema, hostname da plataforma e destino resolvido."""
    partes = urlsplit(url)
    if partes.scheme != "https" or not partes.hostname:
        raise ValueError("URL inválida. Use um link https de vídeo.")

    if partes.hostname.startswith("xn--") or ".xn--" in partes.hostname:
        raise ValueError("Domínio não permitido.")

    if plataforma_da_url(url) is None:
        raise ValueError("Plataforma não suportada. Use Kwai ou TikTok.")

    if not _enderecos_publicos(partes.hostname, partes.port or 443):
        raise ValueError("Destino não permitido.")

    return url
