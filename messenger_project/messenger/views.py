from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView

from .models import Chat, Message
from .forms import ChatForm, MessageForm


class CreateChatView(LoginRequiredMixin, CreateView):
    template_name = 'messenger/create_chat.html'
    form_class = ChatForm
    success_url = reverse_lazy('chat_detail')

    def form_valid(self, form):
        form.instance.admin = self.request.user
        chat = form.save()
        self.success_url = reverse_lazy('chat_detail', kwargs={'chat_id': chat.id})
        return super().form_valid(form)


class ChatDetailView(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        if request.user == chat.admin or request.user in chat.users.all():
            form = MessageForm()
            messages = chat.messages.all()  # Отримати всі повідомлення для цього чату
            return render(request, 'messenger/chat_detail.html', {'chat': chat, 'form': form, 'messages': messages})
        else:
            return redirect('chat_list')  # або інша сторінка з помилкою доступу

    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        if request.user == chat.admin or request.user in chat.users.all():
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.chat = chat
                message.author = request.user
                message.save()
                return redirect('chat_detail', chat_id=chat_id)
            messages = chat.messages.all()  # Отримати всі повідомлення для цього чату
            return render(request, 'messenger/chat_detail.html', {'chat': chat, 'form': form, 'messages': messages})
        else:
            return redirect('chat_list')  # або інша сторінка з помилкою доступу


class AddUserToChatView(View):
    @login_required
    def post(self, request, chat_id, user_id):
        chat = get_object_or_404(Chat, id=chat_id)
        user = get_object_or_404(User, id=user_id)
        if request.user == chat.admin:
            chat.users.add(user)
        return redirect('chat_detail', chat_id=chat_id)


class RemoveUserFromChatView(View):
    @login_required
    def post(self, request, chat_id, user_id):
        chat = get_object_or_404(Chat, id=chat_id)
        user = get_object_or_404(User, id=user_id)
        if request.user == chat.admin:
            chat.users.remove(user)
        return redirect('chat_detail', chat_id=chat_id)


class EditMessageView(View):
    @login_required
    def get(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        if request.user == message.author and (timezone.now() - message.date_sent).days < 1:
            form = MessageForm(instance=message)
            return render(request, 'messenger/edit_message.html', {'form': form})
        else:
            return redirect('chat_list')  # або інша сторінка з помилкою доступу

    @login_required
    def post(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        if request.user == message.author and (timezone.now() - message.date_sent).days < 1:
            form = MessageForm(request.POST, instance=message)
            if form.is_valid():
                form.save()
                return redirect('chat_detail', chat_id=message.chat.id)
            return render(request, 'messenger/edit_message.html', {'form': form})
        else:
            return redirect('chat_list')  # або інша сторінка з помилкою доступу


class DeleteMessageView(View):
    @login_required
    def post(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        if request.user == message.author and (timezone.now() - message.date_sent).days < 1:
            chat_id = message.chat.id
            message.delete()
        return redirect('chat_detail', chat_id=chat_id)
