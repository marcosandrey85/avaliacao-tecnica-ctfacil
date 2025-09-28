# cotefacil_spider.py
import json
import scrapy
import logging
import os
from scrapy import Request, FormRequest


class CotefacilProdutos(scrapy.Spider):
    name = "Geração de produtos"
    token_url = "https://desafio.cotefacil.net/oauth/token"
    produto_url = "https://desafio.cotefacil.net/produto"

    custom_settings = {
        "LOG_LEVEL": "INFO",
        "LOG_FILE": "logs/cotefacil.log", 
        "LOG_ENABLED": True,
    }

    def __init__(self, username=None, password=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not username or not password:
            raise ValueError("Você deve passar username e password: scrapy runspider cotefacil_spider.py -a username=... -a password=...")
        self.username = username
        self.password = password

    def start_requests(self):
        """Faz o POST para obter o token (form-urlencoded)."""
        formdata = {
            "username": self.username,
            "password": self.password,
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        yield FormRequest(
            url=self.token_url,
            formdata=formdata,
            headers=headers,
            callback=self.parse_token,
            errback=self.errback_token,
            dont_filter=True
        )

    def errback_token(self, failure):
        self.logger.error("Erro ao requisitar token: %s", failure)
        return

    def parse_token(self, response):
        """Extrai o token e chama a requisição /produto com Authorization."""
        try:
            data = json.loads(response.text)
        except Exception:
            self.logger.error("Resposta do /oauth/token não é JSON válido:\n%s", response.text)
            return

        access_token = data.get("access_token") or data.get("token") or data.get("accessToken")
        token_type = data.get("token_type") or data.get("type") or "Bearer"

        if not access_token:
            self.logger.error("Não foi possível encontrar access_token na resposta: %s", data)
            return


        auth_header_value = f"{token_type} {access_token}".strip()

        headers = {
            "accept": "application/json",
            "Authorization": auth_header_value
        }

        # GET /produto
        yield Request(
            url=self.produto_url,
            headers=headers,
            callback=self.parse_produto,
            errback=self.errback_produto,
            dont_filter=True
        )

    def errback_produto(self, failure):
        self.logger.error("Erro ao requisitar /produto: %s", failure)
        return

    def parse_produto(self, response):
        """
        Salva o JSON retornado por /produto em produto.json.
        """
        try:
            os.makedirs("data", exist_ok=True)
            data = json.loads(response.text)
            with open("data/produto.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.info("Salvo data/produto.json (%d bytes)", len(response.text.encode("utf-8")))
        except Exception:
            self.logger.warning("/produto não retornou JSON válido")