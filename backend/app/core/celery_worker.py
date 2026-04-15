from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")

celery = Celery(
    "worker",
    broker=f"redis://{REDIS_HOST}:6379/0",
    backend=f"redis://{REDIS_HOST}:6379/0"
)

celery.autodiscover_tasks(["app.authentication.service"])