from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory, Groups, Object, Tests, Standards
from .user import (
    UserInventoryForm,
    UserGroupsForm,
    UserObjectForm,
    UserTestsForm,
    UserStandardsForm,
)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_panel')
                else:
                    return redirect('system_settings')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})
@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect('system_settings')
    return render(request, 'core/admin_panel.html')
# Список инвентаря
@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    return render(request, 'core/inventory_list.html', {'inventories': inventories})

# Создание инвентаря
@login_required
def inventory_create(request):
    if request.method == 'POST':
        form = UserInventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = UserInventoryForm()
    return render(request, 'core/inventory_form.html', {'form': form})

# Редактирование инвентаря
@login_required
def inventory_edit(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = UserInventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = UserInventoryForm(instance=inventory)
    return render(request, 'core/inventory_form.html', {'form': form})

@login_required
def inventory_delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        inventory.delete()
        return redirect('inventory_list')
    return render(request, 'core/inventory_confirm_delete.html', {'inventory': inventory})

# Список групп
@login_required
def groups_list(request):
    groups = Groups.objects.all()
    return render(request, 'core/groups_list.html', {'groups': groups})

@login_required
def groups_create(request):
    if request.method == 'POST':
        form = UserGroupsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('groups_list')
    else:
        form = UserGroupsForm()
    return render(request, 'core/groups_form.html', {'form': form})

@login_required
def groups_edit(request, pk):
    group = get_object_or_404(Groups, pk=pk)
    if request.method == 'POST':
        form = UserGroupsForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('groups_list')
    else:
        form = UserGroupsForm(instance=group)
    return render(request, 'core/groups_form.html', {'form': form})

@login_required
def groups_delete(request, pk):
    group = get_object_or_404(Groups, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('groups_list')
    return render(request, 'core/groups_confirm_delete.html', {'group': group})

@login_required
def object_list(request):
    objects = Object.objects.all()
    return render(request, 'core/object_list.html', {'objects': objects})

@login_required
def object_create(request):
    if request.method == 'POST':
        form = UserObjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('object_list')
    else:
        form = UserObjectForm()
    return render(request, 'core/object_form.html', {'form': form})

@login_required
def object_edit(request, pk):
    obj = get_object_or_404(Object, pk=pk)
    if request.method == 'POST':
        form = UserObjectForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('object_list')
    else:
        form = UserObjectForm(instance=obj)
    return render(request, 'core/object_form.html', {'form': form})

@login_required
def object_delete(request, pk):
    obj = get_object_or_404(Object, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('object_list')
    return render(request, 'core/object_confirm_delete.html', {'object': obj})

@login_required
def tests_list(request):
    tests = Tests.objects.all()
    return render(request, 'core/tests_list.html', {'tests': tests})

@login_required
def tests_create(request):
    if request.method == 'POST':
        form = UserTestsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tests_list')
    else:
        form = UserTestsForm()
    return render(request, 'core/tests_form.html', {'form': form})

@login_required
def tests_edit(request, pk):
    test = get_object_or_404(Tests, pk=pk)
    if request.method == 'POST':
        form = UserTestsForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('tests_list')
    else:
        form = UserTestsForm(instance=test)
    return render(request, 'core/tests_form.html', {'form': form})

# Удаление теста
@login_required
def tests_delete(request, pk):
    test = get_object_or_404(Tests, pk=pk)
    if request.method == 'POST':
        test.delete()
        return redirect('tests_list')
    return render(request, 'core/tests_confirm_delete.html', {'test': test})

# Список стандартов
@login_required
def standards_list(request):
    standards = Standards.objects.all()
    return render(request, 'core/standards_list.html', {'standards': standards})

# Создание стандарта
@login_required
def standards_create(request):
    if request.method == 'POST':
        form = UserStandardsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('standards_list')
    else:
        form = UserStandardsForm()
    return render(request, 'core/standards_form.html', {'form': form})

# Редактирование стандарта
@login_required
def standards_edit(request, pk):
    standard = get_object_or_404(Standards, pk=pk)
    if request.method == 'POST':
        form = UserStandardsForm(request.POST, instance=standard)
        if form.is_valid():
            form.save()
            return redirect('standards_list')
    else:
        form = UserStandardsForm(instance=standard)
    return render(request, 'core/standards_form.html', {'form': form})

# Удаление стандарта
@login_required
def standards_delete(request, pk):
    standard = get_object_or_404(Standards, pk=pk)
    if request.method == 'POST':
        standard.delete()
        return redirect('standards_list')
    return render(request, 'core/standards_confirm_delete.html', {'standard': standard})

@login_required
def edit_db(request):
    if not request.user.is_staff:
        return redirect('system_settings')

    # Получаем все инвентари
    inventories = Inventory.objects.all()

    # Получаем выбранный инвентарь из GET-параметров
    selected_inventory_id = request.GET.get('inventory')
    print("Selected inventory ID:", selected_inventory_id)  # Отладочный вывод

    # Преобразуем selected_inventory_id в целое число
    try:
        selected_inventory_id = int(selected_inventory_id) if selected_inventory_id else None
    except ValueError:
        print("Ошибка: Некорректное значение inventory")
        selected_inventory_id = None

    # Фильтруем группы по выбранному инвентарю
    groups = []
    if selected_inventory_id:
        try:
            groups = Groups.objects.filter(id_i_id=selected_inventory_id)
            print("Filtered groups:", groups)  # Отладочный вывод
        except Exception as e:
            print("Ошибка при фильтрации групп:", e)  # Отладочный вывод
            raise

    # Передаем данные в шаблон
    return render(request, 'core/edit_db.html', {
        'inventories': inventories,
        'groups': groups,
        'selected_inventory_id': selected_inventory_id,
    })
@login_required
def system_settings(request):
    return render(request, 'core/system_settings.html')

@login_required
def save_object(request):
    if request.method == 'POST':
        group_id = request.POST.get('group')
        subgroup_id = request.POST.get('subgroup')
        object_id = request.POST.get('object')

        standards = request.POST.getlist('standard')
        requirements = request.POST.getlist('requirement')

        tests = request.POST.getlist('test')
        recommendations = request.POST.getlist('recommendation')
        metrics = request.POST.getlist('metric')

        # Создаем объект
        group = Groups.objects.get(id_g=group_id)
        obj = Object.objects.create(id_g=group, название="Новый объект")

        # Создаем стандарты
        for standard, requirement in zip(standards, requirements):
            Standards.objects.create(id_o=obj, стандарт=standard, требование=requirement)

        # Создаем тесты
        for test, recommendation, metric in zip(tests, recommendations, metrics):
            Tests.objects.create(
                id_o=obj,
                испытание=test,
                рекомендация=recommendation,
                метрика=float(metric)
            )

        return redirect('edit_db')
    return redirect('edit_db')


@login_required
def regulations(request):
    inventories = Inventory.objects.all()
    groups = []
    objects = []
    standards = []
    unmet_requirements = []
    all_met = False
    show_requirements = False

    selected_inventory = request.POST.get('inventory') or request.GET.get('inventory')
    selected_group = request.POST.get('group') or request.GET.get('group')
    selected_object = request.POST.get('object') or request.GET.get('object')

    if selected_inventory:
        groups = Groups.objects.filter(id_i=selected_inventory)

    if selected_group:
        objects = Object.objects.filter(id_g=selected_group)

    # Загружаем стандарты сразу, если объект выбран
    if selected_object:
        standards = Standards.objects.filter(id_o=selected_object)
    else:
        standards = []  # Если объект не выбран, стандартов нет

    # Проверяем, была ли нажата кнопка "Продолжить"
    if request.method == 'POST' and 'continue_button' in request.POST:
        show_requirements = True

        # Получаем ID выбранных стандартов (может быть пустым)
        completed_ids = request.POST.getlist('standard_checkbox')

        # Если объект выбран, продолжаем проверку
        if selected_object:
            if not completed_ids:
                # Если ничего не отмечено → все стандарты считаются невыполненными
                unmet_requirements = standards
            else:
                # Иначе считаем невыполненными те, которых нет среди отмеченных
                unmet_requirements = [std for std in standards if str(std.id_s) not in completed_ids]

            all_met = len(unmet_requirements) == 0

    context = {
        'inventories': inventories,
        'groups': groups,
        'objects': objects,
        'standards': standards,
        'unmet_requirements': unmet_requirements,
        'all_met': all_met,
        'selected_inventory': selected_inventory,
        'selected_group': selected_group,
        'selected_object': selected_object,
        'show_requirements': show_requirements,
    }

    return render(request, 'core/regulations.html', context)
@login_required
def definition(request):
    inventories = Inventory.objects.all()

    selected_inventory_id = request.GET.get('inventory')
    groups = Groups.objects.filter(id_i=selected_inventory_id) if selected_inventory_id else []

    selected_group_id = request.GET.get('group')
    tests = Tests.objects.filter(id_o__id_g=selected_group_id).select_related('id_o') if selected_group_id else []

    selected_test_ids = request.GET.getlist('test')
    objects = Object.objects.filter(tests__id_def__in=selected_test_ids).distinct() if selected_test_ids else []

    verdict = None
    if request.method == 'POST':
        selected_test_ids = request.POST.getlist('test')
        objects = Object.objects.filter(tests__id_def__in=selected_test_ids).distinct()
        verdict = "Объект определен." if objects else "Не удалось определить объект."

    return render(request, 'core/definition.html', {
        'inventories': inventories,
        'groups': groups,
        'tests': tests,
        'objects': objects,
        'verdict': verdict,
        'selected_inventory_id': int(selected_inventory_id) if selected_inventory_id else None,
        'selected_group_id': int(selected_group_id) if selected_group_id else None,
    })

@login_required
def defects(request):
    inventories = Inventory.objects.all()

    selected_inventory_id = request.GET.get('inventory')
    groups = Groups.objects.filter(id_i=selected_inventory_id) if selected_inventory_id else []

    selected_group_id = request.GET.get('group')
    objects = Object.objects.filter(id_g=selected_group_id) if selected_group_id else []

    selected_object_id = request.GET.get('object')
    tests = Tests.objects.filter(id_o=selected_object_id).select_related('id_o') if selected_object_id else []

    discrepancies = []
    recommendations = {}
    show_results = False

    if request.method == 'POST':
        show_results = True

        for test in tests:
            metric_key = f'metric_{test.id_def}'
            entered_value = request.POST.get(metric_key)

            try:
                entered_value_float = float(entered_value)
                if abs(entered_value_float - test.метрика) > 1e-9:  # защита от float погрешности
                    discrepancies.append(test)
                    recommendations[test.id_def] = test.рекомендация
            except (ValueError, TypeError):
                # Если пользователь не ввёл число или оно невалидно
                discrepancies.append(test)
                recommendations[test.id_def] = test.рекомендация

    return render(request, 'core/defects.html', {
        'inventories': inventories,
        'groups': groups,
        'objects': objects,
        'tests': tests,
        'show_results': show_results,
        'discrepancies': discrepancies,
        'recommendations': recommendations,
        'selected_inventory_id': int(selected_inventory_id) if selected_inventory_id else None,
        'selected_group_id': int(selected_group_id) if selected_group_id else None,
        'selected_object_id': int(selected_object_id) if selected_object_id else None,
    })