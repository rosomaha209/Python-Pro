from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Chat, Message
from .forms import ChatForm, MessageForm


@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    can_create_chat = request.user.has_perm('messenger.can_create_chat')
    can_change_chat = request.user.has_perm('messenger.can_change_chat')
    return render(request, 'messenger/chat_list.html', {'chats': chats, 'can_create_chat': can_create_chat,
                                                        'can_change_chat': can_change_chat})  # Додайте can_change_chat до контексту


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
def edit_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if not message.can_edit(request.user):
        return redirect('chat_detail', chat_id=message.chat.id)

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('chat_detail', chat_id=message.chat.id)
    else:
        form = MessageForm(instance=message)
    return render(request, 'messenger/edit_message.html', {'form': form})


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if message.can_edit(request.user) and message.can_delete(request.user):
        message.delete()
    return redirect('chat_detail', chat_id=message.chat.pk)


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
