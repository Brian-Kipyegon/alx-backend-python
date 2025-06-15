from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old_message = Message.objects.filter(pk=instance.pk).first()
        if old_message and old_message.content != instance.content:
            MessageHistory.objects.create(
                message=instance, old_content=old_message.content
            )
            instance.edited = True


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Clean up messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Clean up notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Clean up message history where user was involved
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
