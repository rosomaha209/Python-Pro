from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.signals import request_started, request_finished
from .models import Message, Chat


@receiver(pre_save, sender=Message)
def message_pre_save(sender, instance, **kwargs):
    print("До оновлення повідомлення")


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if created:
        print("Повідомлення створено")
    else:
        print("Повідомлення оновлено")


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
