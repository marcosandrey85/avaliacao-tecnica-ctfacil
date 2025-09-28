# worker.py
from rq import Worker, Queue
from redis import Redis
from tasks import processar_usuario


redis_conn = Redis()
queue = Queue(connection=redis_conn)

if __name__ == "__main__":
    worker = Worker([queue])
    print("Worker iniciado, aguardando jobs...")
    worker.work()
