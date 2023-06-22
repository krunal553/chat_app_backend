from django.contrib import admin
from .models import Thread, UserMessage

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'timestamp']

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'thread', 'sender', 'body', 'file', 'timestamp']