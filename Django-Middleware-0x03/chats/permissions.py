from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to
    view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only participants of the conversation can access the message
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
