from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView

from .my_forms import MemberForm
from .models import Member
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def input_page(request):
    if request.method == 'POST':
        # Створення форми на основі POST-даних
        register_form = MemberForm(request.POST)
        login_form = AuthenticationForm(request, request.POST)
        # Перевірка валідності форми
        if register_form.is_valid():
            # Збереження даних в базу даних
            register_form.save()
            # Перенаправлення на сторінку виведення
            return redirect('output_page')
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # Встановлення сесійних даних
            request.session['name'] = username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Передавання об'єкта користувача до функції login()
                return redirect('output_page')
            else:
                return HttpResponse("Invalid login")
    else:
        # Ініціалізуєм порожню форму
        register_form = MemberForm()
        login_form = AuthenticationForm()

    return render(request, 'members_app/input.html', {'register_form': register_form, 'login_form': login_form})


def output_page(request):
    # Отримання всіх об'єктів з моделі Member
    members = Member.objects.all()
    # Перевірка, чи є об'єкти
    if members:
        # Відображення шаблону з отриманими об'єктами
        return render(request, 'members_app/output.html', {'members': members})
    else:
        # Перенаправлення на сторінку вводу
        return redirect('input_page')


def session_page(request):
    if request.method == 'POST':
        # Очищення сесійних даних
        request.session.flush()
        #  розавторизація користувача
        logout(request)
        # Перенаправлення на сторінку курсів
        return redirect('courses_page')

    # Отримуємо дані з сесії
    name = request.session.get('name', 'Anonymous')
    email = request.session.get('email', 'None')
    return render(request, 'members_app/session.html', {'name': name, 'email': email})
