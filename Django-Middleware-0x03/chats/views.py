from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404

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
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            "conversation__conversation_id": ["exact"],
            "sender__username": ["exact"],
        }


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        user = self.request.user
        queryset = Message.objects.filter(conversation__participants=user)
        return queryset

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        message = self.get_object()
        if self.request.user != message.sender:
            raise PermissionDenied("You are not allowed to update this message.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.sender:
            raise PermissionDenied("You are not allowed to delete this message.")
        instance.delete()
