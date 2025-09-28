Avaliação Técnica Cotefácil - BASICA

Aplicação de web scraping desenvolvida em Python com Scrapy.
O objetivo é autenticar na API pública
https://desafio.cotefacil.net/docs, obter todos os produtos disponíveis
e salvar o resultado em /data/produto.json.

------------------------------------------------------------------------

Tecnologias utilizadas

-   Python 3.10+
-   Poetry – gerenciamento de dependências
-   Scrapy – framework de scraping
-   Redis - 


------------------------------------------------------------------------

Pré-requisitos

Antes de começar, você precisa ter instalado em sua máquina:

-   Python 3.10 ou superior
-   Poetry
-   Redis (servidor local ativo)
-   RQ 



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





##----------------------------------------------------------------------##
Avaliação Técnica Cotefácil - INTERMEDIARIA

2. Instale RQ e Redis Python client:
   poetry add rq redis

3. Instale e configure o Redis no sistema:
   sudo apt update
   sudo apt install redis-server -y
   sudo systemctl start redis
   sudo systemctl enable redis

> O Redis precisa estar ativo para que o worker consiga processar os jobs.

Estrutura do Projeto:
- utils/tasks.py – Funções que processam usuários e enviam produtos para a API.
- utils/worker.py – Worker do RQ que processa os jobs da fila.
- utils/enviar_dado_fila.py – Script para enfileirar usuários e senhas na fila via terminal.
- data/produto.json – Arquivo com os produtos a serem enviados.

Observações importantes:

1. Limite de envio de produtos:
   No arquivo utils/tasks.py, linha 102:
      produtos = produtos[:100]

   - Essa linha limita o envio a 100 produtos para não sobrecarregar a API de teste.
   - Para enviar todos os produtos do JSON, basta comentar ou remover essa linha.

2. Logs do Scrapy:
   - O log padrão de inicialização do Scrapy foi configurado para exibir apenas WARNINGS/ERROS, mantendo o log limpo.
   - Logs detalhados estão disponíveis em logs/work.log.

Como rodar a aplicação:

1. Inicie o worker do RQ:
   python utils/worker.py

2. Enfileire um usuário para processamento:
   python utils/enviar_dado_fila.py --usuario <usuario> --senha <senha>

- Você pode substituir --usuario e --senha pelos dados desejados.
- O worker irá processar o job, cadastrando o usuário (ou realizando login) e enviando os produtos.

Observações finais:
- Certifique-se de que o Redis está ativo antes de enfileirar jobs.
- O envio dos produtos depende do token obtido via cadastro ou login do usuário.
- Logs de envio e falhas podem ser consultados em logs/work.log.


👨‍💻 Autor

Feito para avaliação técnica Cotefácil 
