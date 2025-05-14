from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import UserProfile

# Главная страница
@login_required
def home(request):
    return render(request, 'core/home.html')

# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, user_type='regular')  # По умолчанию обычный пользователь
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

# Авторизация пользователя
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

# Добавление нового пользователя администратором
@login_required
def add_user(request):
    if request.user.userprofile.user_type != 'admin':
        return redirect('home')  # Только администраторы могут добавлять пользователей

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = request.POST.get('user_type', 'regular')
            UserProfile.objects.create(user=user, user_type=user_type)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'core/add_user.html', {'form': form})