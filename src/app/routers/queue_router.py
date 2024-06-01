from rq import Queue
from redis import Redis
import importlib
from fastapi import APIRouter

# Queue and Worker
redis_conn = Redis(host='redis-internal', port=6379)
queue = Queue('default', connection=redis_conn)
router = APIRouter()


@router.get("/submit-job/")
async def enqueue_task(function_name: str, *args, **kwargs):
    try:
        module = importlib.import_module("processors")
        func = getattr(module, function_name)
        job = queue.enqueue(func, *args, **kwargs)
        return {"job_id": job.id, "status": job.get_status()}
    except (ModuleNotFoundError, AttributeError) as e:
        return {"error": str(e)}
