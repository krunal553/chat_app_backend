from django.contrib import admin
from .models import Thread, UserMessage

admin.site.register(Thread)
admin.site.register(UserMessage)