from django.contrib import admin
from .models import Message, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'timestamp', 'edited')
    list_filter = ('edited', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'edited_by', 'edited_at', 'old_content')
    list_filter = ('edited_at',)
    search_fields = ('old_content', 'message__id', 'edited_by__username')
