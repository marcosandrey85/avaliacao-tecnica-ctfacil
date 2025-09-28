# enqueue.py
import argparse
from rq import Queue
from redis import Redis
from tasks import processar_usuario  # IMPORTAÇÃO CORRETA

# Configurar argparse
parser = argparse.ArgumentParser(description="Enfileirar usuário no RQ")
parser.add_argument("--usuario", required=True, help="Nome do usuário")
parser.add_argument("--senha", required=True, help="Senha do usuário")
args = parser.parse_args()

# Conectar ao Redis
redis_conn = Redis()  # localhost:6379
q = Queue(connection=redis_conn)

# Dado no formato dict
dado = {
    "usuario": args.usuario,
    "senha": args.senha
}

# Enfileirar o job
job = q.enqueue(processar_usuario, dado)
print(f"Job enfileirado com ID: {job.id}")
