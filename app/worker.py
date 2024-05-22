from celery import Celery
from config import Config
from redis import Redis
from redis.lock import Lock as RedisLock

celery = Celery(__name__, include=["infrastructure.tasks"])
celery.config_from_object(Config, namespace="CELERY")
celery.task_track_started = True
celery.result_persistent = True

redis_instance = Redis.from_url(Config.CELERY_BROKER_URL)
lock = RedisLock(redis_instance, name="task_id")

REDIS_TASK_KEY = "current_task"
