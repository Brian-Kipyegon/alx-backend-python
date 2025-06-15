from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from messaging.models import Message


@cache_page(60)
@login_required
def threaded_conversation(request):
    messages = Message.objects.filter(sender=request.user) | Message.objects.filter(
        receiver=request.user
    )
    messages = messages.select_related(
        "sender", "receiver", "parent_message"
    ).prefetch_related("replies")

    return render(
        request, "messaging/threaded_conversation.html", {"messages": messages}
    )
