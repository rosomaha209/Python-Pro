from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .mixins import MessageEditDeleteMixin, SuperuserRequiredMixin
from .models import Chat, Message
from .forms import ChatForm, MessageForm


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    context_object_name = 'chats'
    template_name = 'messenger/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)


class CreateChatView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Chat
    form_class = ChatForm
    success_url = reverse_lazy('chat_list')
    template_name = 'messenger/create_chat.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.participants.add(self.request.user)
        return response


class EditChatView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chat
    form_class = ChatForm
    template_name = 'messenger/edit_chat.html'
    success_url = reverse_lazy('chat_list')

    def test_func(self):
        chat = self.get_object()
        return self.request.user.has_perm('messenger.change_chat') or self.request.user.is_superuser or chat.participants.filter(id=self.request.user.id).exists()

    def get_object(self, queryset=None):
        chat_id = self.kwargs.get('chat_id')
        return get_object_or_404(Chat, pk=chat_id)

    def handle_no_permission(self):
        raise PermissionDenied

class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    context_object_name = 'chat'
    template_name = 'messenger/chat_detail.html'


class SendMessageView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, pk=chat_id)
        Message.objects.create(
            chat=chat,
            author=request.user,
            content=request.POST.get('content')
        )
        return redirect('chat_detail', pk=chat_id)


class EditMessageView(LoginRequiredMixin, MessageEditDeleteMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messenger/edit_message.html'

    def get_success_url(self):
        return reverse_lazy('chat_detail', kwargs={'chat_id': self.object.chat.pk})


class DeleteMessageView(LoginRequiredMixin, MessageEditDeleteMixin, DeleteView):
    model = Message
    template_name = 'messenger/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('chat_detail', kwargs={'chat_id': self.object.chat.pk})

    def get_queryset(self):
        # Ця перевірка забезпечує, що користувач може видаляти лише свої повідомлення
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    can_create_chat = request.user.has_perm('messenger.can_create_chat')
    can_change_chat = request.user.has_perm('messenger.can_change_chat')
    return render(request, 'messenger/chat_list.html', {'chats': chats, 'can_create_chat': can_create_chat,
                                                        'can_change_chat': can_change_chat})


@login_required
def edit_chat(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)

    if not request.user.has_perm('messenger.change_chat') and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = ChatForm(request.POST, instance=chat)
        if form.is_valid():
            form.save()
            return redirect('chat_list')
    else:
        form = ChatForm(instance=chat)

    return render(request, 'messenger/edit_chat.html', {'form': form})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    if request.user in chat.participants.all():
        messages = chat.messages.all()
        messages_with_authorship = []
        for message in messages:
            can_edit_or_delete = False
            if message.can_edit(request.user):
                can_edit_or_delete = True
            messages_with_authorship.append((message, can_edit_or_delete))
        return render(request, 'messenger/chat_detail.html', {'chat': chat, 'messages': messages_with_authorship})
    else:
        return redirect('chat_list')


@login_required
def create_chat(request):
    if not request.user.has_perm('messenger.can_create_chat') and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save()
            chat.participants.add(request.user)
            return redirect('chat_list')
    else:
        form = ChatForm()
    return render(request, 'messenger/create_chat.html', {'form': form})


@login_required
def add_user_to_chat(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.get(username=username)
        chat.participants.add(user)
        return redirect('chat_detail', chat_id=chat_id)
    else:
        return render(request, 'messenger/add_user_to_chat.html', {'chat': chat})


@login_required
def send_message(request, chat_id):
    if request.method == 'POST':
        chat = Chat.objects.get(pk=chat_id)
        content = request.POST['content']
        author = request.user
        message = Message.objects.create(chat=chat, author=author, content=content)
    return redirect('chat_detail', chat_id=chat_id)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def remove_participant(request, chat_id, participant_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    participant = get_object_or_404(User, pk=participant_id)
    chat.participants.remove(participant)
    return redirect('chat_detail', chat_id=chat_id)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration_form.html'
