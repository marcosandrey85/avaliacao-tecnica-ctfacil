import scrapy
import json
import os
from scrapy.crawler import CrawlerProcess
import urllib.parse



class ProdutoSpider(scrapy.Spider):
    name = "produto_dynamic_post"

    signup_url = "https://desafio.cotefacil.net/oauth/signup"
    login_url = "https://desafio.cotefacil.net/oauth/token"
    produto_url = "https://desafio.cotefacil.net/produto"
    produto_file = "data/produto.json"

    def __init__(self, usuario, senha, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = usuario
        self.password = senha

    def start_requests(self):
        self.logger.info(f"Iniciando processo para usuário {self.username}")
        payload = {"username": self.username, "password": self.password}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        # Tenta cadastrar usuário
        yield scrapy.Request(
            url=self.signup_url,
            method="POST",
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse_signup,
            meta={"payload": payload, "headers": headers}
        )

    def parse_signup(self, response):
        print(response)
        self.logger.info(f"Resposta do signup: {response.meta['payload']}")
        self.logger.info(f"Resposta do signup: {response.text}")
        payload = response.meta["payload"]
        payload_str = urllib.parse.urlencode(payload)

        headers = {"accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded"}

        token = None
        try:
            data = json.loads(response.text)
            token = data.get("token")
        except Exception:
            self.logger.warning("Não foi possível extrair token do signup")

        if "Usuário já registrado." in response.text or response.status == 200:
            if not token:
                self.logger.info("Usuário já registrado, tentando login...")
                yield scrapy.Request(
                    url=self.login_url,
                    method="POST",
                    headers=headers,
                    body=payload_str,
                    callback=self.parse_login,
                    meta={"payload": payload_str, "headers": headers}
                )
            else:
                self.logger.info("Token obtido no signup, enviando produtos...")
                yield from self.enviar_produtos(token)
        else:
            self.logger.error(f"Falha no cadastro: {response.text}")

    def parse_login(self, response):
        self.logger.info(f"Resposta do login: {response.text}")
        token = None
        try:
            data = json.loads(response.text)
            token = data.get("access_token")
        except Exception:
            self.logger.error("Não foi possível extrair token do login")

        if token:
            self.logger.info("Token obtido no login, enviando produtos...")
            yield from self.enviar_produtos(token)
        else:
            self.logger.error("Falha no login, não é possível enviar produtos")

    def enviar_produtos(self, token):
        self.logger.info(f"Lendo produtos de {self.produto_file}")
        if not os.path.exists(self.produto_file):
            self.logger.error(f"Arquivo {self.produto_file} não encontrado.")
            return

        with open(self.produto_file, "r", encoding="utf-8") as f:
            produtos = json.load(f)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        self.logger.info(f"Enviando {len(produtos)} produtos...")
        produtos = produtos[:100]
        for produto in produtos:
            self.logger.info(f"Enviando produto: {produto.get('nome', '')}")
            yield scrapy.Request(
                url=self.produto_url,
                method="POST",
                headers=headers,
                body=json.dumps(produtos),
                callback=self.parse_resposta_produto,
                meta={"produto": produtos}
            )

    def parse_resposta_produto(self, response):
        produto = response.meta["produto"]
        if response.status == 200:
            self.logger.info(f"Produto  enviado com sucesso!")
        else:
            self.logger.warning(f"Falha ao enviar produto")


# Função chamada pelo RQ
def processar_usuario(dado: dict):
    usuario = dado.get("usuario")
    senha = dado.get("senha")
    print(f"Processando usuário: {usuario} com senha: {senha}")

    process = CrawlerProcess(settings={
        "LOG_LEVEL": "INFO",
        "LOG_FILE": "logs/work.log",
        "LOG_ENABLED": True,
        "STATS_DUMP": False,    
        "TELNETCONSOLE_ENABLED": False,
        "HTTPERROR_ALLOWED_CODES": [400, 401, 403, 404, 422]
    })

    process.crawl(ProdutoSpider, usuario=usuario, senha=senha)
    process.start()
