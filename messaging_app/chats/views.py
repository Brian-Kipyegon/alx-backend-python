from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationFilter(filters.FilterSet):
    class Meta:
        model = Conversation
        fields = {
            "participants__username": ["exact"],
        }


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ConversationFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(
            self.get_serializer(message).data, status=status.HTTP_201_CREATED
        )
