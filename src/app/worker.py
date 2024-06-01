import redis
from rq import Worker, Queue, Connection
from app.models._base_model import _metadata_obj
from app.db.database import PSQLManager

listen = ['default']
redis_url = 'redis://redis-internal:6379'
conn = redis.from_url(redis_url)

_metadata_obj.create_all(bind=PSQLManager.Instance().get_base_engin(), checkfirst=True)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()