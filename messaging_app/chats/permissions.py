from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to access or modify its messages/conversation.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        elif isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        return False
