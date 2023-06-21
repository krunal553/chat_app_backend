from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile
from chat.models import Thread, UserMessage
from chat.serializers import ThreadSerializer, MessageSerializer, FilteredMessageSerializer
from rest_framework import status
from django.db.models import Q


@api_view(['GET'])
def get_routes(request):
    routes = [
        'create-thread/',
        'create/',
    ]
    return Response(routes)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_or_create_thread(request):
    sender = request.user.profile
    recipient_id = request.data.get('recipient_id')
    recipient = UserProfile.objects.get(id=recipient_id)
    if recipient_id is not None:
        try:
            # thread, created = Thread.objects.get_or_create(sender=sender, receiver=recipient)
            user_thread = Thread.objects.filter(
                Q(sender=sender, receiver=recipient) | Q(sender=recipient, receiver=sender)
            )
            if user_thread.exists():
                thread = user_thread.first()
            else:
                thread = Thread.objects.create(sender=sender, receiver=recipient)

            serializer = ThreadSerializer(thread, many=False, context={'request': request, 'thread': thread})
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'detail':'User with that id doesnt not exists'})
    else:
        return Response({'details':'Recipient id not found'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_message(request):
    sender = request.user.profile
    data = request.data
    receiver = UserProfile.objects.get(username=data.get('username'))
    if receiver:
        message = data.get('message')
        thread = Thread.objects.filter(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
        ).first()
        if thread:
            if message is not None:
                message = UserMessage.objects.create(thread=thread, sender=sender, body=message)
                message.save()
                serializer = MessageSerializer(message, many=False)
                return Response(serializer.data)
            else:
                return Response({'details':'Content for message required'})
        else:
            return Response({'details':'Thread not found'})
    else:
        return Response({'details':'Please provide other user id'})
    

# @api_view(['GET'])
# def read_messages(request, pk):
#     try:
#         thread = Thread.objects.get(thread_id=pk)
#         un_read = thread.messages.filter(is_read=False)
#         for msg in un_read:
#             msg.is_read = True
#             msg.save()
#         messages = thread.messages.all()
#         serializer = MessageSerializer(messages, many=True)
#         return Response(serializer.data)
#     except Exception as e:
#         return Response({'details': f"{e}"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def read_messages(request, username):
    try:
        user = request.user.profile
        user_to_chat_with = UserProfile.objects.get(username=username)
        thread = Thread.objects.filter(
            Q(sender=user, receiver=user_to_chat_with) | Q(sender=user_to_chat_with, receiver=user)
        ).first()        
        messages = thread.messages
        if thread.sender == user or thread.receiver == user:
            if thread.sender == user:
                messages = thread.messages.filter(deleted_by_thread_sender=None)
            elif thread.receiver == user:
                messages = thread.messages.filter(deleted_by_thread_receiver=None)
            for message in messages:
                if message.sender != user:
                    message.is_read = True
                    message.save()

            # serializer = FilteredMessageSerializer(
            #     messages, many=True, 
            #     context={'request': request, 'thread': thread, 'user': user}
            # )
            serializer = FilteredMessageSerializer(messages, many=True)
            return Response(serializer.data)
        else:
            return Response({'details': 'You do not have permission to read this thread.'},
                            status=status.HTTP_403_FORBIDDEN)
    except Thread.DoesNotExist:
        return Response({'details': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_messages(request, username):
    try:
        user = request.user.profile
        user_to_chat_with = UserProfile.objects.get(username=username)
        thread = Thread.objects.filter(
            Q(sender=user, receiver=user_to_chat_with) | Q(sender=user_to_chat_with, receiver=user)
        ).first() 

        messages = thread.messages
        
        if thread.sender == user:
            messages.filter(deleted_by_thread_sender=None).update(deleted_by_thread_sender=user)
            return Response(MessageSerializer(messages, many=True).data)
        elif thread.receiver == user:
            messages.filter(deleted_by_thread_receiver=None).update(deleted_by_thread_receiver=user)
            return Response(MessageSerializer(messages, many=True).data)

            
        return Response({'detail': 'You are not authorized to delete this message.'}, status=status.HTTP_403_FORBIDDEN)
        

    except Exception as e:
            return Response({'details': f"{e}"},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user_threads(request):
    user = request.user.profile
    # user = UserProfile.objects.get(user=usr)
    threads = Thread.objects.filter(Q(sender=user) | Q(receiver=user))
    serializer = ThreadSerializer(threads, many=True, context={'request': request, 'user': user})
    return Response(serializer.data)

# chat thread b/w meet and krunal
# a75b9be6-5568-4e63-ac4c-2d70874e54a1


# sample apis

@api_view(['GET'])
def get_messages(request):
    thread = request.query_params.get('thread')
    messages = UserMessage.objects.filter(thread=thread)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_messages(requrst):
    msgs = UserMessage.objects.all()
    serializer = MessageSerializer(msgs, many=True)
    # serializer = FilteredMessageSerializer(msgs, many=True, context={'request': request, 'thread': thread, 'user': user})

    return Response(serializer.data)

@api_view(['GET'])
def get_all_threads(requrst):
    thread = Thread.objects.all()
    serializer = ThreadSerializer(thread, many=True)
    return Response(serializer.data)

