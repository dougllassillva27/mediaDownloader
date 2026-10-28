"""
Testes de segurança das rotas: validação de URL de plataforma, confinamento do
arquivo baixado no diretório temporário e limite do upload do conversor.
"""
import socket
import os

import pytest
from fastapi.testclient import TestClient

import main
import routes.api as api
from services.url_service import plataforma_da_url, validar_url_plataforma
from services.download_service import _dentro_do_temp, _nome_interno, download_media_async
from scraper import sanitize_filename

client = TestClient(main.app)


def resolver_para(monkeypatch, endereco):
    def falso_getaddrinfo(host, porta, *args, **kwargs):
        return [(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", (endereco, porta or 443))]

    monkeypatch.setattr(socket, "getaddrinfo", falso_getaddrinfo)


class TestPlataformaDaUrl:
    def test_aceita_hosts_das_plataformas(self):
        assert plataforma_da_url("https://www.kwai.com/@usuario/video/123") == "kwai.com"
        assert plataforma_da_url("https://kwai.com/@usuario/video/123") == "kwai.com"
        assert plataforma_da_url("https://vm.tiktok.com/ZMhKjExample/") == "tiktok.com"
        assert plataforma_da_url("https://www.tiktok.com/@usuario/video/1") == "tiktok.com"

    def test_recusa_substring_da_plataforma_fora_do_host(self):
        assert plataforma_da_url("http://127.0.0.1:8099/media.mp4?kwai.com") is None
        assert plataforma_da_url("https://atacante.example/?kwai.com") is None
        assert plataforma_da_url("https://atacante.example/kwai.com/video") is None

    def test_recusa_sufixo_falso(self):
        assert plataforma_da_url("https://kwai.com.atacante.example/v") is None
        assert plataforma_da_url("https://naokwai.com/v") is None
        assert plataforma_da_url("https://tiktok.com.br.example/v") is None

    def test_recusa_entrada_vazia(self):
        assert plataforma_da_url("") is None
        assert plataforma_da_url(None) is None


class TestValidarUrlPlataforma:
    def test_rejeita_esquema_nao_https(self):
        with pytest.raises(ValueError):
            validar_url_plataforma("http://www.kwai.com/@u/video/1")

    def test_rejeita_host_fora_das_plataformas(self):
        with pytest.raises(ValueError):
            validar_url_plataforma("https://atacante.example/video.mp4")

    def test_rejeita_destino_privado(self, monkeypatch):
        resolver_para(monkeypatch, "127.0.0.1")
        with pytest.raises(ValueError):
            validar_url_plataforma("https://www.kwai.com/@u/video/1")

    def test_rejeita_destino_link_local(self, monkeypatch):
        resolver_para(monkeypatch, "169.254.169.254")
        with pytest.raises(ValueError):
            validar_url_plataforma("https://www.kwai.com/@u/video/1")

    def test_aceita_host_publico(self, monkeypatch):
        resolver_para(monkeypatch, "93.184.216.34")
        url = "https://www.kwai.com/@usuario/video/123"
        assert validar_url_plataforma(url) == url


class TestRotasDeDownload:
    def test_rejeita_url_de_host_arbitrario(self):
        resposta = client.get(
            "/api/download/mp4",
            params={"url": "https://127.0.0.1/media.mp4", "filename": "video"},
        )
        assert resposta.status_code == 400

    def test_rejeita_url_com_substring_da_plataforma(self):
        resposta = client.get(
            "/api/download/mp3",
            params={"url": "https://atacante.example/media.mp4?kwai.com", "filename": "audio"},
        )
        assert resposta.status_code == 400

    def test_rejeita_esquema_file(self):
        resposta = client.get(
            "/api/download/mp4",
            params={"url": "file:///etc/passwd", "filename": "video"},
        )
        assert resposta.status_code == 400


class TestRotasDeInfo:
    def test_recusa_url_de_host_interno_com_substring(self):
        resposta = client.post(
            "/api/info",
            data={"url": "http://127.0.0.1:8099/media.mp4?kwai.com"},
        )
        corpo = resposta.json()
        assert corpo["success"] is False
        assert "suportada" in corpo["error"].lower() or "inv" in corpo["error"].lower()


class TestNomeDoArquivo:
    def test_sanitiza_nome_do_cliente(self):
        assert "/" not in sanitize_filename("../escaped")
        assert ".." not in sanitize_filename("../escaped")
        assert ".." not in sanitize_filename("/tmp/abs-escaped")

    def test_nome_interno_nao_usa_entrada_do_usuario(self):
        nome = _nome_interno()
        assert nome.startswith("media_")
        assert "/" not in nome and ".." not in nome

    def test_confinamento_no_temp(self):
        assert _dentro_do_temp(os.path.join("temp", "arquivo.mp4")) is True
        assert _dentro_do_temp(os.path.join("temp", "..", "escapou.mp4")) is False
        assert _dentro_do_temp("/tmp/fora.mp4") is False

    def test_download_usa_nome_interno_e_devolve_nome_sanitizado(self, monkeypatch):
        capturado = {}

        def falso_download(url, format_type, temp_filename):
            capturado["temp_filename"] = temp_filename
            caminho = os.path.join("temp", f"{temp_filename}.mp4")
            open(caminho, "wb").write(b"dummy")
            return caminho

        monkeypatch.setattr("services.download_service._download_media", falso_download)
        resultado = __import__("asyncio").run(
            download_media_async("https://www.kwai.com/@u/video/1", "mp4", "../escapou")
        )
        assert capturado["temp_filename"].startswith("media_")
        assert "/" not in capturado["temp_filename"] and ".." not in capturado["temp_filename"]
        assert "/" not in resultado["filename"] and ".." not in resultado["filename"]
        assert resultado["filename"].endswith(".mp4")
        os.remove(resultado["path"])


class TestLimiteDoUpload:
    def test_aborta_upload_acima_do_limite_sem_gravar_arquivo(self, monkeypatch):
        monkeypatch.setattr(api, "LIMITE_UPLOAD_BYTES", 1024 * 1024)
        antes = sorted(os.listdir("temp"))
        resposta = client.post(
            "/api/convert",
            files={"file": ("video.mp4", b"\x00" * (2 * 1024 * 1024), "video/mp4")},
        )
        depois = sorted(os.listdir("temp"))

        assert resposta.status_code == 400
        assert "grande" in resposta.json()["detail"].lower()
        assert antes == depois

    def test_rejeita_extensao_fora_da_allowlist(self):
        resposta = client.post(
            "/api/convert",
            files={"file": ("script.sh", b"#!/bin/sh\n", "text/plain")},
        )
        assert resposta.status_code == 400
