# core/views.py

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

# Главная страница (админская панель)
@login_required
def admin_panel(request):
    return render(request, 'core/admin_panel.html')

# Авторизация пользователя
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:  # Если пользователь — администратор
                return redirect('admin_panel')
            else:  # Если пользователь — обычный пользователь
                return redirect('system_settings')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# Добавление нового пользователя администратором
@login_required
def add_user(request):
    # Проверка прав доступа: только администраторы могут добавлять пользователей
    if not request.user.is_staff:
        return redirect('admin_panel')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data['is_admin']  # Установка права администратора
            user.save()
            return redirect('admin_panel')  # Перенаправление на админскую панель
    else:
        form = RegisterForm()
    return render(request, 'core/add_user.html', {'form': form})

# Редактирование базы данных
@login_required
# core/views.py

@login_required
def edit_db(request):
    # Проверка прав доступа: только администраторы могут редактировать БД
    if not request.user.is_staff:
        return redirect('admin_panel')

    context = {
        'message': 'Здесь будет интерфейс для редактирования базы данных.'
    }
    return render(request, 'core/edit_db.html', context)

# Настройки системы
@login_required
def system_settings(request):
    # Проверка прав доступа: только администраторы могут изменять настройки системы
    if not request.user.is_staff:
        return redirect('admin_panel')

    # Пример данных для отображения (замените на реальные настройки системы)
    context = {
        'message': 'Здесь будут настройки системы.'
    }
    return render(request, 'core/system_settings.html', context)

@login_required
def regulations(request):
    return render(request, 'core/regulations.html')

@login_required
def definition(request):
    return render(request, 'core/definition.html')

@login_required
def defects(request):
    return render(request, 'core/defects.html')