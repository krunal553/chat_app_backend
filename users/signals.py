from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.dispatch import Signal, receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, username=instance.username, name=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Creating Signals
notification = Signal()

# Receiver Functions
@receiver(notification)
def send_notification(sender, **kwargs):
   
    channel_layer = get_channel_layer()
    room_group_name = f"user_{sender.id}"

    # Send message to the room group
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'user_message',
            'message': {"type": "new_message"},
        }
    )