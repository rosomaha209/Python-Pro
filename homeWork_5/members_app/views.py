from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView

from .my_forms import MemberForm
from .models import Member
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def input_page(request):
    if request.method == 'POST':
        # ��������� ����� �� ����� POST-�����
        register_form = MemberForm(request.POST)
        login_form = AuthenticationForm(request, request.POST)
        # �������� �������� �����
        if register_form.is_valid():
            # ���������� ����� � ���� �����
            register_form.save()
            # ��������������� �� ������� ���������
            return redirect('output_page')
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # ������������ ������� �����
            request.session['name'] = username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # ����������� ��'���� ����������� �� ������� login()
                return redirect('output_page')
            else:
                return HttpResponse("Invalid login")
    else:
        # ��������� ������� �����
        register_form = MemberForm()
        login_form = AuthenticationForm()

    return render(request, 'members_app/input.html', {'register_form': register_form, 'login_form': login_form})


def output_page(request):
    # ��������� ��� ��'���� � ����� Member
    members = Member.objects.all()
    # ��������, �� � ��'����
    if members:
        # ³���������� ������� � ���������� ��'������
        return render(request, 'members_app/output.html', {'members': members})
    else:
        # ��������������� �� ������� �����
        return redirect('input_page')


def session_page(request):
    if request.method == 'POST':
        # �������� ������� �����
        request.session.flush()
        #  �������������� �����������
        logout(request)
        # ��������������� �� ������� �����
        return redirect('courses_page')

    # �������� ��� � ���
    name = request.session.get('name', 'Anonymous')
    email = request.session.get('email', 'None')
    return render(request, 'members_app/session.html', {'name': name, 'email': email})
