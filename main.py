import scrapy
from scrapy.http import FormRequest
import os

class ServimedLoginSpider(scrapy.Spider):
    name = "servimed_login"
    allowed_domains = ["pedidoeletronico.servimed.com.br"]
    start_urls = ["https://pedidoeletronico.servimed.com.br/login"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = os.getenv("SERVIMED_USERNAME")
        self.password = os.getenv("SERVIMED_PASSWORD")

    def parse(self, response):
        self.logger.info(f"URL: {response.url}")
        self.logger.debug(f"HTML inicial: {response.text[:200]}")
        
        if response.status != 200:
            self.logger.error(f"Erro ao acessar a página de login: {response.status}")
            return


        formdata = {
            "username": self.username,
            "password": self.password,
        }

        yield FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.after_login,
            dont_filter=True,
            formxpath='//form', 
        )

    def after_login(self, response):
        if response.xpath('//a[contains(text(), "Sair")]'):
            self.logger.info("Login bem-sucedido!")
            yield response.follow("/Pedido", callback=self.parse_pedidos)
        else:
            self.logger.error("Falha no login, confira nomes dos campos.")
            with open("login_failed.html", "wb") as f:
                f.write(response.body)

    def parse_pedidos(self, response):
        for row in response.xpath('//table[contains(@class, "pedidos")]//tr[td]'):
            id_text = row.xpath("./td[1]//text()").get(default="").strip()
            cliente_text = row.xpath("./td[2]//text()").get(default="").strip()
            if id_text and cliente_text:
                yield {
                    "id": id_text,
                    "cliente": cliente_text,
                }