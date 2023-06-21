from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import UserMessage
from django.dispatch import Signal


# @receiver(post_save, sender=UserMessage)
# def send_notification_on_message_create(sender, instance, created, updated=False, **kwargs):
#     if created or updated:
#         send_notification(instance)
#     else:
#         send_notification(instance)


# def send_notification(instance):

#     channel_layer = get_channel_layer()
#     sender_id = instance.thread.sender.id
#     receiver_id = instance.thread.receiver.id

#     # Create the message payload
#     message = {
#         'id': str(instance.id),
#         'sender': str(sender_id),
#         'receiver': str(receiver_id),
#         # Add any other necessary fields from the UserMessage model
#         # to the message payload
#     }

#     # Send the message to the sender's channel
#     async_to_sync(channel_layer.group_send)(
#         f'user_{sender_id}',
#         {'type': 'user_message', 'message': "message"}
#     )

#     # Send the message to the receiver's channel
#     async_to_sync(channel_layer.group_send)(
#         f'user_{receiver_id}',
#         {'type': 'user_message', 'message': message}
#     )

def send_notification(sender_id, receiver_id):

    channel_layer = get_channel_layer()
    # sender_id = instance.thread.sender.id
    # receiver_id = instance.thread.receiver.id

    # Create the message payload
    # message = {
    #     'id': str(instance.id),
    #     'sender': str(sender_id),
    #     'receiver': str(receiver_id),
    #     # Add any other necessary fields from the UserMessage model
    #     # to the message payload
    # }

    # Send the message to the sender's channel
    async_to_sync(channel_layer.group_send)(
        f'user_{sender_id}',
        {'type': 'user_message', 'message': "message"}
    )

    # Send the message to the receiver's channel
    async_to_sync(channel_layer.group_send)(
        f'user_{receiver_id}',
        {'type': 'user_message', 'message': "message"}
    )


notification_signal = Signal()

@receiver(notification_signal)
def send_notification_receiver(sender, **kwargs):

    # if kwargs['instance']:
    instance = kwargs['instance']
    sender_id = instance.sender.id
    receiver_id = instance.receiver.id

    send_notification(sender_id=sender_id,receiver_id=receiver_id)