from log import logger
from redis import Redis
from constants.config import settings

class QueueResourceInternal():
    def __init__(self):
        self.redis_db = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
        

    def post(self, item, queuename):
        try:
            val = self.redis_db.rpush(queuename, item)
            logger.info("added {} items to : {}".format(1, queuename))
            logger.info("queue len {} items : {}".format(str(val), queuename))
            return {"message": "success"}
        except:
            return {"message": "fail"}
    
    def get(self, queuename):
        try:
            l = self.redis_db.lrange(queuename, 0, -1)
            logger.info("returned {} item from queue {}".format(str(l), queuename))
            return l
        except:
            logger.info("error when get item from queue {}".format(queuename))
            return None