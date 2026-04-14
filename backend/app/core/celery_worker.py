from celery import Celery
import app.authentication.service
import app.ingestion.service

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)