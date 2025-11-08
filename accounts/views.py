from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        data_nascimento = request.POST['data_nascimento']
        avatar = request.POST['avatar']
        personagem = request.POST['personagem']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe!')
        else:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(
                user=user,
                email=email,
                data_nascimento=data_nascimento,
                avatar=avatar,
                personagem=personagem,
            )
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.username}!')
            return redirect('/')  # ✅ Redireciona para a página inicial
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')
