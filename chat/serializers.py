from rest_framework import serializers
from .models import UserMessage, Thread
from users.serializers import UserProfileSerializer
from datetime import datetime
import pytz


class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)

    class Meta:
        model = UserMessage
        fields = '__all__'


class FilteredMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField(read_only=True)
    timestamp = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserMessage
        fields = ['sender','body', 'file', 'timestamp',]

    def get_sender(self, obj):
        sender = UserProfileSerializer(obj.sender, many=False).data
        # print(sender)
        return {
            "username": sender['username'],
            "profile_pic": sender['profile_pic']
        }
    def get_timestamp(self, obj):
        utc_time = obj.timestamp
        ist_tz = pytz.timezone('Asia/Kolkata')
        ist_time = utc_time.astimezone(ist_tz)

        # django_date_format = '%m/%d/%Y, %I:%M:%S %p'
        # django_date_format = '%m/%d/%Y, %I:%M %p'
        django_date_format = '%I:%M %p'

        ist_date_string = ist_time.strftime(django_date_format)

        # print(react_date_string)  # Output: 05/25/2023, 04:34:34 PM
        return ist_date_string


class ThreadSerializer(serializers.ModelSerializer):
    user_to_chat_with = serializers.SerializerMethodField(read_only=True)
    last_message = serializers.SerializerMethodField(read_only=True)
    un_read_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Thread
        fields = ['thread_id', 'timestamp', 'user_to_chat_with', 'last_message', 'un_read_count']

    def get_last_message(self, obj):
        user = self.context['request'].user.profile
        if obj.sender == user:
            message = obj.messages.filter(deleted_by_thread_sender=None).order_by('timestamp').last()
        elif obj.receiver == user:
            message = obj.messages.filter(deleted_by_thread_receiver=None).order_by('timestamp').last()

        # message = obj.messages.order_by('timestamp').last()
        serializer = MessageSerializer(message, many=False)
        return serializer.data

    def get_un_read_count(self, obj):
        un_read_count = obj.messages.filter(is_read=False).count()
        return un_read_count
    
    def get_user_to_chat_with(self, obj):
        user = self.context['request'].user.profile
        if obj.sender != user:
            return UserProfileSerializer(obj.sender, many=False).data
        else:
            return UserProfileSerializer(obj.receiver, many=False).data



#  {
#     "id": "82c68f10-b7da-4d26-b8b9-efe1a2c4e283",
#     "name": null,
#     "username": "shivansh",
#     "profile_pic": "/default.png",
#     "bio": null,
#     "user": 5,
#     "followers": []
#   }