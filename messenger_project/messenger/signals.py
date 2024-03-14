import logging
from datetime import datetime

from django.contrib.auth import user_logged_in, user_logged_out
from django.core.signals import request_finished, request_started
from django.db.models.signals import (m2m_changed, post_delete, post_save,
                                      pre_delete, pre_save)
from django.dispatch import receiver

from .models import Chat, Message

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"Користувач {user.username} увійшов у систему о {now}."
    logger.info(log_message)
    print(log_message)


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"Користувач {user.username} вийшов з системи о {now}."
    logger.info(log_message)
    print(log_message)


@receiver(pre_save, sender=Message)
def message_pre_save(sender, instance, **kwargs):
    print("До оновлення повідомлення")


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if created:
        # перевіряємо, чи є серед учасників чату суперюзер
        instance.to_superuser = instance.chat.participants.filter(is_superuser=True).exists()
        instance.save()
        # Логуємо відправлення повідомлення
        logger.info(f"Повідомлення від {instance.author.username} у чаті {instance.chat}: {instance.text}")


@receiver(pre_delete, sender=Message)
def message_pre_delete(sender, instance, **kwargs):
    print(f"Повідомлення з id {instance.pk} буде видалено.")


@receiver(post_delete, sender=Message)
def message_post_delete(sender, instance, **kwargs):
    print(f"Повідомлення з id {instance.pk} видалено.")


# m2m_changed сигнал для ManyToManyField на моделі Chat
@receiver(m2m_changed, sender=Chat.participants.through)
def chat_participants_changed(sender, instance, action, pk_set, **kwargs):
    if action in ["pre_add", "post_add"]:
        print(f"Учасників додано до чату {instance.pk}: {pk_set}")
    elif action in ["pre_remove", "post_remove"]:
        print(f"Учасників видалено з чату {instance.pk}: {pk_set}")


@receiver(request_started)
def request_started_signal(sender, environ, **kwargs):
    pass


@receiver(request_finished)
def request_finished_signal(sender, **kwargs):
    pass
