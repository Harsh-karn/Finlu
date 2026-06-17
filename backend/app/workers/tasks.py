from celery import Celery
from app.config import settings

celery_app = Celery(
    "flowmoney_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def send_budget_alert_email(email: str, category: str, usage_percent: float):
    print(f"Simulating sending budget alert email to {email} for category {category}. Usage: {usage_percent}%")
    return True
