from rest_framework import serializers
from .models import User, Conversation, Message


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "conversation",
            "sender",
            "sender_username",
            "message_body",
            "sent_at",
        ]


# Conversation Serializer with Nested Messages
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    # Custom field example using SerializerMethodField
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
            "last_message",
        ]

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-sent_at").first()
        if last_msg:
            return last_msg.message_body
        return None

    # Example of custom validation with ValidationError
    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least two participants."
            )
        return value
