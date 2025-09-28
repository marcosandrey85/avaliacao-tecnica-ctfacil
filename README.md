Avaliação Técnica Cotefácil

Aplicação de web scraping desenvolvida em Python com Scrapy.
O objetivo é autenticar na API pública
https://desafio.cotefacil.net/docs, obter todos os produtos disponíveis
e salvar o resultado em /data/produto.json.

------------------------------------------------------------------------

Tecnologias utilizadas

-   Python 3.10+
-   Poetry – gerenciamento de dependências
-   Scrapy – framework de scraping

------------------------------------------------------------------------

Pré-requisitos

Antes de começar, você precisa ter instalado em sua máquina:

-   Python 3.10 ou superior
-   Poetry

Para instalar o Poetry:

    curl -sSL https://install.python-poetry.org | python3 -

Verifique a instalação:

    poetry --version

------------------------------------------------------------------------

Instalação

Clone o repositório e instale as dependências com o Poetry:

    git clone https://github.com/seu-usuario/avaliacao-tecnica-ctfacil.git
    cd avaliacao-tecnica-ctfacil

    poetry install

Ative o ambiente virtual:

    poetry shell

------------------------------------------------------------------------

Executando o spider

O spider não faz parte de um projeto Scrapy completo, então ele é
executado com runspider.

Exemplo de execução:

    scrapy runspider cotefacil_spider.py -a username=<seu_usuario> -a password=<sua_senha>

Parâmetros obrigatórios

-   username → usuário de login
-   password → senha de login


------------------------------------------------------------------------

Saída dos dados

Após a execução, os produtos retornados pela API serão salvos em:

    /data/produto.json

Formato do arquivo: JSON, identado e com UTF-8.

------------------------------------------------------------------------

Logs

Durante a execução, os logs são salvos em:

    /logs/cotefacil.log

Além disso, também são exibidos no console.

------------------------------------------------------------------------

Exemplo de uso completo

    scrapy runspider cotefacil_spider.py   -a username=usuario@example.com   -a password=senha123  

------------------------------------------------------------------------

 Documentação da API

Para mais detalhes sobre os endpoints utilizados:
https://desafio.cotefacil.net/docs

------------------------------------------------------------------------

👨‍💻 Autor

Feito para avaliação técnica Cotefácil 
