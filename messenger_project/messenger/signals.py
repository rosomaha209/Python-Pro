import logging

from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.signals import request_started, request_finished
from .models import Message, Chat

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    logger.info(f"Користувач {user} увійшов у систему.")


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    logger.info(f"Користувач {user} вийшов з системи.")


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
