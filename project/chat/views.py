from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import TemplateView, View, ListView
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest

from chat.models import Chat, Message
from chat.forms import MessageForm
from chat_users.models import FriendRequest

User = get_user_model()


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = dict()
        query = request.GET.get('user-search', None)
        if query:
            user = User.objects.filter(email=query)
            if user.exists():
                context['search'] = user.first()
                return render(request, 'home.html', context)
            elif not user.exists():
                context['no_user'] = 'No user with this email'

        return render(request, 'home.html', context)


class InboxView(View):
    def get(self, request, chat_id, *args, **kwargs):
        chat = get_object_or_404(Chat, id=chat_id)
        context = dict(chat=chat)
        form = MessageForm()
        context['form'] = form
        return render(request, 'chat.html', context)

    def post(self, request, chat_id, *args, **kwargs):
        chat = get_object_or_404(Chat, id=chat_id)
        participants_list = list(chat.participants.all())
        participants_list.remove(request.user)
        receiver = participants_list[0]
        context = dict(chat=chat)
        form = MessageForm(request.POST)
        if request.user not in receiver.friends.all():
            return HttpResponseBadRequest()

        if form.is_valid():
            message_instance = form.save(commit=False)
            message_instance.user = request.user
            message_instance.save()
            chat.messages.add(message_instance)
            return redirect(reverse('chat', args=[chat.id]))

        context['form'] = form
        return render(request, 'chat.html', context)


class ChatListView(ListView):
    template_name = 'chat_list.html'
    model = Chat
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.filter(participants__in=[self.request.user])

