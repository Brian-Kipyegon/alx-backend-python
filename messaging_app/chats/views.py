from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


class ConversationFilter(filters.FilterSet):
    class Meta:
        model = Conversation
        fields = {
            "participants__username": ["exact"],
        }


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ConversationFilter
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        conversation.participants.add(request.user)
        return Response(
            self.get_serializer(conversation).data, status=status.HTTP_201_CREATED
        )


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            "conversation__conversation_id": ["exact"],
            "sender__username": ["exact"],
        }


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(sender=request.user)
        return Response(
            self.get_serializer(message).data, status=status.HTTP_201_CREATED
        )
