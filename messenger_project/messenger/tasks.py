from celery import shared_task, Celery
from .models import Message
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)
app = Celery('tasks', broker='redis://redis:6379/0')


@shared_task
def task():
    print('task')


@shared_task
def log_recent_messages():
    time_threshold = timezone.now() - timezone.timedelta(minutes=5)
    recent_messages = Message.objects.filter(created_at__gte=time_threshold).order_by('-created_at')[:10]
    logger.info("Останні 10 повідомлень за останні 5 хвилин:")
    for message in recent_messages:
        logger.info(f"{message.created_at.strftime('%Y-%m-%d %H:%M:%S')} - {message.author.username}: {message.text}")
