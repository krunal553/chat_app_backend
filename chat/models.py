import uuid
from django.utils import timezone
from django.db import models
from users.models import UserProfile
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

class Thread(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sender_thread")
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="receiver_thread")
    # timestamp = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender', 'receiver'], name='unique_thread')
        ]

    def __str__(self):
        return f"{self.sender} and {self.receiver}"
    
    def clean(self):
        if self.sender == self.receiver:
            raise ValidationError("Sender and receiver cannot be the same user.")

        if Thread.objects.filter(sender=self.receiver, receiver=self.sender).exists():
            raise ValidationError("A thread between these users already exists.")

class UserMessage(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    file = models.FileField(upload_to='message_files/', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mp3', 'avi', 'mov'])])
    is_read = models.BooleanField(default=False)
    # timestamp = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)
    deleted_by_thread_sender = models.ForeignKey(
        UserProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="deleted_messages_sender"
    )
    deleted_by_thread_receiver =  models.ForeignKey(
        UserProfile, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name="deleted_messages_receiver"
    )

    def __str__(self):
        if self.file:
            return f"{self.sender}: {self.body} [File: {self.file.name}]"
        else:
            return f"{self.sender}: {self.body}"