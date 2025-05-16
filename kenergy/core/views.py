# core/views.py
import logging

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import FactsDetermination, Object, Groups, Inventory, FactsDefects

logger = logging.getLogger(__name__)
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
                logger.info(f"Администратор {user.username} вошел в систему.")
                return redirect('admin_panel')
            else:  # Если пользователь — обычный пользователь
                logger.info(f"Пользователь {user.username} вошел в систему.")
                return redirect('system_settings')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


# Добавление нового пользователя администратором
@login_required
def add_user(request):
    if not request.user.is_staff:
        logger.warning(
            f"Пользователь {request.user.username} попытался добавить нового пользователя, но не имеет прав."
        )
        return redirect('admin_panel')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                logger.info(f"Администратор {request.user.username} создал пользователя {user.username}.")
                return redirect('admin_panel')
            except Exception as e:
                logger.error(f"Ошибка при создании пользователя: {e}")
                return render(request, 'core/add_user.html', {
                    'form': form,
                    'error_message': 'Произошла ошибка при создании пользователя.'
                })
        else:
            # Логируем ошибки валидации
            logger.error(f"Ошибка валидации формы: {form.errors}")
            # Передаем форму с ошибками обратно в шаблон
            return render(request, 'core/add_user.html', {'form': form})
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

    context = {
        'message': 'Здесь будут настройки системы.'
    }
    return render(request, 'core/system_settings.html', context)

@login_required
def regulations(request):
    return render(request, 'core/regulations.html')

@login_required
def definition(request):
    # Получаем все группы
    groups = Groups.objects.all()

    # Если выбрана группа, получаем её подгруппы
    selected_group_id = request.GET.get('group')
    subgroups = Groups.objects.filter(id_i=selected_group_id) if selected_group_id else []

    # Если выбрана подгруппа, получаем её факты
    selected_subgroup_id = request.GET.get('subgroup')
    facts = FactsDetermination.objects.filter(id_o__id_g=selected_subgroup_id).select_related('id_o') if selected_subgroup_id else []

    # Если выбран факт, определяем объект
    selected_fact_ids = request.GET.getlist('fact')  # Получаем список выбранных фактов
    objects = Object.objects.filter(factsdetermination__id_d__in=selected_fact_ids).distinct() if selected_fact_ids else []

    context = {
        'groups': groups,
        'subgroups': subgroups,
        'facts': facts,
        'objects': objects,
        'selected_group_id': int(selected_group_id) if selected_group_id else None,
        'selected_subgroup_id': int(selected_subgroup_id) if selected_subgroup_id else None,
    }

    return render(request, 'core/definition.html', context)

@login_required
@login_required
def defects(request):
    # Получаем все группы
    groups = Groups.objects.all()

    # Если выбрана группа, получаем её подгруппы
    selected_group_id = request.GET.get('group')
    subgroups = Groups.objects.filter(id_i=selected_group_id) if selected_group_id else []

    # Если выбрана подгруппа, получаем её объекты
    selected_subgroup_id = request.GET.get('subgroup')
    objects = Object.objects.filter(id_g=selected_subgroup_id) if selected_subgroup_id else []

    # Если выбран объект, получаем его дефекты из модели FactsDefects
    selected_object_id = request.GET.get('object')
    defects = FactsDefects.objects.filter(id_o=selected_object_id).select_related('id_o') if selected_object_id else []

    # Если нажата кнопка "Проверить пригодность"
    if request.method == 'POST':
        selected_defect_ids = request.POST.getlist('defect')  # Получаем список выбранных дефектов
        verdict = "Пригоден" if not selected_defect_ids else "Не пригоден"
        return render(request, 'core/defects.html', {
            'groups': groups,
            'subgroups': subgroups,
            'objects': objects,
            'defects': defects,
            'verdict': verdict,
            'selected_group_id': int(selected_group_id) if selected_group_id else None,
            'selected_subgroup_id': int(selected_subgroup_id) if selected_subgroup_id else None,
            'selected_object_id': int(selected_object_id) if selected_object_id else None,
        })

    # Если GET-запрос, отображаем форму
    return render(request, 'core/defects.html', {
        'groups': groups,
        'subgroups': subgroups,
        'objects': objects,
        'defects': defects,
        'verdict': None,
        'selected_group_id': int(selected_group_id) if selected_group_id else None,
        'selected_subgroup_id': int(selected_subgroup_id) if selected_subgroup_id else None,
        'selected_object_id': int(selected_object_id) if selected_object_id else None,
    })