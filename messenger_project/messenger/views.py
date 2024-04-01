import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)

from messenger.forms import (FileUploadForm, MessageForm, TextFileForm,
                             UserPermissionForm)
from messenger.mixins import (AdminOrPermissionRequiredMixin,
                              UserCanEditMessageMixin, UserIsAuthorMixin)
from messenger.models import Chat, Message, UploadedFile, User, UserStatus


class ChatCreateView(AdminOrPermissionRequiredMixin, CreateView):
    model = Chat
    fields = ['name', 'participants']
    template_name = 'messenger/create_chat.html'
    success_url = reverse_lazy('chat_list')
    permission_required = 'messenger.can_create_chat'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Чат було успішно створено.')
        return response

    def handle_no_permission(self):
        messages.error(self.request, 'У вас недостатньо прав для виконання цієї дії.')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


class ChatDeleteView(UserPassesTestMixin, DeleteView):
    model = Chat
    success_url = reverse_lazy('chat_list')

    def test_func(self):
        return self.request.user.has_perm('messenger.can_delete_chat') or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'У вас недостатньо прав для виконання цієї дії.')
        return redirect('chat_list')


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'messenger/chat_list.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'messenger/chat_detail.html'
    context_object_name = 'chat'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MessageForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat = self.get_object()
            message.chat = self.object
            message.to_superuser = message.chat.participants.filter(is_superuser=True).exists()
            message.save()

            if message.to_superuser:
                messages.info(request, "Ви успішно надіслали повідомлення суперюзеру.")

            return redirect('chat_detail', pk=message.chat.pk)
        return self.render_to_response(self.get_context_data(form=form))


class MessageUpdateView(UserCanEditMessageMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messenger/edit_message.html'

    def get_success_url(self):
        return self.object.chat.get_absolute_url()


class MessageDeleteView(UserIsAuthorMixin, DeleteView):
    model = Message
    template_name = 'messenger/confirm_delete.html'
    success_url = reverse_lazy(
        'chat_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class ChatAddParticipantView(UserPassesTestMixin, UpdateView):
    model = Chat
    template_name = 'messenger/chat_add_participant.html'
    fields = ['participants']
    success_url = reverse_lazy('chat_list')

    def test_func(self):
        return self.request.user.is_superuser


class ChatRemoveParticipantView(AdminOrPermissionRequiredMixin, View):
    raise_exception = True
    permission_required = 'messenger.can_remove_participants'

    def post(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, pk=kwargs.get('chat_id'))
        user_to_remove = get_object_or_404(User, pk=request.POST.get('user_id'))
        chat.participants.remove(user_to_remove)
        return redirect('chat_detail', pk=chat.pk)

    def handle_no_permission(self):
        messages.error(self.request, 'у вас недостатньо прав для виконання цієї дії.')
        return redirect(self.request.META.get('HTTP_REFERER', 'chat_list'))


class UserPermissionView(UserPassesTestMixin, FormView):
    template_name = 'messenger/user_permissions.html'
    form_class = UserPermissionForm
    success_url = reverse_lazy('user_permissions')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.save_permissions()
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'у вас недостатньо прав для виконання цієї дії.')
        return redirect(self.request.META.get('HTTP_REFERER', 'chat_list'))


class MessageCreateView(CreateView):
    model = Message
    fields = ['text']
    template_name = 'messenger/create_message.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.chat_id = self.kwargs['chat_id']
        response = super().form_valid(form)

        return response

    def get_success_url(self):
        return reverse_lazy('chat_detail', kwargs={'pk': self.kwargs['chat_id']})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_permissions'] = self.request.user.get_user_permissions()
        return context


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

    def post(self, request, *args, **kwargs):
        messages.info(request, "Ви вийшли з системи.")
        super().post(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('login'))


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration_form.html'


class FileUploadView(FormView):
    template_name = 'messenger/file_upload.html'
    form_class = FileUploadForm
    success_url = reverse_lazy('file_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class FileListView(ListView):
    model = UploadedFile
    template_name = 'messenger/file_list.html'
    context_object_name = 'files'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        files_with_types = []
        files_to_remove = []

        for file in context['files']:
            file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

            # Перевіряємо, чи існує файл на диску
            if not os.path.exists(file_path):
                files_to_remove.append(file)
                continue

            file_info = {
                'file': file,
                'file_type': 'other',
                'content': ''  # Інформація про вміст
            }

            if file.file.url.lower().endswith(('.mp3', '.wav')):
                file_info['file_type'] = 'audio'
            elif file.file.url.lower().endswith('.mp4'):
                file_info['file_type'] = 'video'
            elif file.file.url.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_info['file_type'] = 'image'
            elif file.file.url.lower().endswith('.txt'):
                file_info['file_type'] = 'text'
                # Читання вмісту текстового файлу
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_info['content'] = f.read()
                except IOError:
                    file_info['content'] = "Неможливо прочитати файл."

            files_with_types.append(file_info)

        # Видалення записів про відсутні файли
        for file in files_to_remove:
            file.delete()

        context['files_with_types'] = files_with_types
        return context


class EditTextView(FormView):
    template_name = 'messenger/edit_text_file.html'
    form_class = TextFileForm

    def get_initial(self):
        file_id = self.kwargs.get('file_id')
        file = UploadedFile.objects.get(pk=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                content = f.read()
        except IOError:
            raise Http404("Помилка при читанні файлу.")

        # Нормалізація символів кінця рядка
        content = content.replace('\r\n', '\n')
        return {'content': content}

    def form_valid(self, form):
        file_id = self.kwargs.get('file_id')
        file = UploadedFile.objects.get(pk=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
        content = form.cleaned_data['content']

        # Вибір символа кінця рядка
        content = content.replace('\r\n', '\n').replace('\r', '\n')

        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('file_list')


def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def user_status_api(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        print('Chat not found')
        return JsonResponse({'error': 'Чат не знайдено'}, status=404)

    chat_user_ids = chat.participants.values_list('id', flat=True)

    statuses = UserStatus.objects.filter(user_id__in=chat_user_ids).select_related('user')

    for status in statuses:
        status.check_if_user_is_active()

    user_statuses = [{'user_id': status.user.id, 'is_online': status.is_online} for status in statuses]
    return JsonResponse(user_statuses, safe=False)


