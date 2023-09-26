from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from .models import UserMessage, Thread
from .serializers import MessageSerializer, ThreadSerializer
from users.models import UserProfile
import uuid
from users.signals import notification

@api_view(['GET'])
def get_routes(request):
    routes = [
        'create-thread/',
        'create/',
    ]
    return Response(routes)

# class ReadMessageApiView(ListCreateAPIView):
#     queryset = UserMessage.objects.all()
#     serializer_class = MessageSerializer

class MessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post (self, request, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user.profile)
            thread = Thread.objects.get(id=request.data.get('thread'))
            notification.send(sender=thread.sender)
            notification.send(sender=thread.receiver)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get (self, request, pk=None, format=None):
        user = request.user.profile
        try:
            thread = Thread.objects.get(id=pk)
        except Thread.DoesNotExist:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        if thread.sender == user or thread.receiver == user:
            
            messages = thread.messages
            if thread.sender == user:
                messages = messages.exclude(deleted_by_thread_sender=user)
            elif thread.receiver == user:
                messages = messages.exclude(deleted_by_thread_receiver=user)
            for message in messages:
                if message.sender != user:
                    message.is_read = True
                    message.save()
            serializer = MessageSerializer(messages, many=True)
            notification.send(sender=thread.sender)
            notification.send(sender=thread.receiver)
            return Response(serializer.data)
        return Response([])
        
    def patch (self, request, pk=None, format=None):
        user = request.user.profile
        try:
            thread = Thread.objects.get(id=pk)
        except Thread.DoesNotExist:
            return Response({'detail': 'Thread not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if thread.sender == user:
            messages = thread.messages.exclude(deleted_by_thread_sender=user)
            messages.update(deleted_by_thread_sender=user)
            notification.send(sender=user)

        elif thread.receiver == user:
            messages = thread.messages.exclude(deleted_by_thread_receiver=user)
            messages.update(deleted_by_thread_receiver=user)  
            notification.send(sender=user)

        else:
            return Response({'detail': 'You are not authorized to delete messages in this thread.'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'detail': 'Messages deleted successfully.'}, status=status.HTTP_200_OK)


class ThreadAPIView(APIView):
    def get (self, request, format=None):
        user = request.user.profile
        threads = Thread.objects.filter(Q(sender=user) | Q(receiver=user))
        serializer = ThreadSerializer(threads, many=True, context={'request': request, 'user': user})
        # sorted_threads = sorted(serializer.data, key=lambda t: t['last_message']['timestamp'])

        return Response(serializer.data)

    def post(self, request):
        receiver = UserProfile.objects.filter(id=request.data.get('receiver_id')).first()
        sender = request.user.profile
        # try:
        #     receiver_uuid = uuid.UUID(receiver_id)
        # except ValueError:
        #     return Response("Invalid receiver_id format.", status=status.HTTP_400_BAD_REQUEST)

        if sender == receiver:
            return Response({"detail":"Sender and receiver cannot be the same user."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            thread = Thread.objects.get(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))
            serializer = ThreadSerializer(thread, many=False, context={'request': request, 'thread': thread})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Thread.DoesNotExist:
            thread = Thread(sender=sender, receiver=receiver)
            thread.save()
            serializer = ThreadSerializer(thread, many=False, context={'request': request, 'thread': thread})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def post(self, request):
    #     serializer = ThreadSerializer(data=request.data, context={'request': request})

    #     if serializer.is_valid():
    #         sender = request.user.profile
    #         receiver = serializer.validated_data['receiver']

    #         if sender == receiver:
    #             return Response({"detail": "Sender and receiver cannot be the same user."}, status=status.HTTP_400_BAD_REQUEST)

    #         thread = Thread.objects.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)).first()
    #         if thread:
    #             serializer = ThreadSerializer(thread, many=False, context={'request': request, 'thread': thread})
    #             return Response(serializer.data, status=status.HTTP_200_OK)

    #         thread = Thread.objects.create(sender=sender, receiver=receiver)
    #         serializer = ThreadSerializer(thread, many=False, context={'request': request, 'thread': thread})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
