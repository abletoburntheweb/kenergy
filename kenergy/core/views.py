import sys

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory, Groups as GroupsModel, Object, Tests, Standards
from .user import (
    UserInventoryForm,
    UserGroupForm,
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
@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    return render(request, 'core/inventory_list.html', {'inventories': inventories})

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
    groups = GroupsModel.objects.all()
    return render(request, 'core/groups_list.html', {'groups': groups})

@login_required
def groups_create(request):
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('groups_list')
    else:
        form = UserGroupForm()
    return render(request, 'core/groups_form.html', {'form': form})

@login_required
def groups_edit(request, pk):
    group = get_object_or_404(GroupsModel, pk=pk)
    if request.method == 'POST':
        form = UserGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('groups_list')
    else:
        form = UserGroupForm(instance=group)
    return render(request, 'core/groups_form.html', {'form': form})

@login_required
def groups_delete(request, pk):
    group = get_object_or_404(GroupsModel, pk=pk)
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
    inventories = Inventory.objects.all()
    selected_inventory_id = request.GET.get('inventory')
    if selected_inventory_id:
        groups = GroupsModel.objects.filter(id_i_id=selected_inventory_id)
    else:
        groups = []
    context = {
        'inventories': inventories,
        'groups': groups,
        'selected_inventory_id': selected_inventory_id,
    }
    return render(request, 'core/edit_db.html', context)

def get_inventories(request):
    inventories = Inventory.objects.all().values('id_i', 'название')
    return JsonResponse(list(inventories), safe=False)

def get_groups(request):
    inventory_id = request.GET.get('inventory')
    groups = GroupsModel.objects.filter(id_i=inventory_id).values('id_g', 'название')

def get_objects(request):
    group_id = request.GET.get('group')
    objects = Object.objects.filter(id_g=group_id).values('id_o', 'название')
    return JsonResponse(list(objects), safe=False)
@login_required
def system_settings(request):
    return render(request, 'core/system_settings.html')

@login_required
def save_object(request):
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory')
        group_id = request.POST.get('group')
        object_id = request.POST.get('object')
        standards = request.POST.getlist('standard[]')
        requirements = request.POST.getlist('requirement[]')
        tests = request.POST.getlist('test[]')
        recommendations = request.POST.getlist('recommendation[]')
        metrics = request.POST.getlist('metric[]')

        if not inventory_id or not group_id:
            return redirect('edit_db')

        inventory = Inventory.objects.get(id_i=inventory_id)
        group = GroupsModel.objects.get(id_g=group_id)

        if object_id:
            obj = Object.objects.get(id_o=object_id)
            obj.id_g = group
            obj.save()
        else:
            obj = Object.objects.create(id_g=group, название="Новый объект")

        for standard, requirement in zip(standards, requirements):
            Standards.objects.create(id_o=obj, стандарт=standard, требование=requirement)

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

    selected_inventory_id = request.GET.get('inventory')
    selected_group_id = request.GET.get('group')
    objects = []
    standards = []

    if selected_inventory_id:
        groups = GroupsModel.objects.filter(id_i=selected_inventory_id)
    else:
        groups = []

    if selected_group_id:
        objects = Object.objects.filter(id_g=selected_group_id)
        standards = Standards.objects.filter(id_o__in=objects)

    context = {
        'inventories': inventories,
        'groups': groups,
        'objects': objects,
        'standards': standards,
        'selected_inventory_id': int(selected_inventory_id) if selected_inventory_id else None,
        'selected_group_id': int(selected_group_id) if selected_group_id else None,
    }

    return render(request, 'core/regulations.html', context)

@login_required
def definition(request):
    inventories = Inventory.objects.all()

    selected_inventory_id = request.GET.get('inventory')
    groups = GroupsModel.objects.filter(id_i=selected_inventory_id) if selected_inventory_id else []

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
    groups = GroupsModel.objects.filter(id_i=selected_inventory_id) if selected_inventory_id else []

    selected_group_id = request.GET.get('group')
    objects = Object.objects.filter(id_g=selected_group_id) if selected_group_id else []

    selected_object_id = request.GET.get('object')
    tests = Tests.objects.filter(id_o=selected_object_id).select_related('id_o') if selected_object_id else []

    verdict = None
    if request.method == 'POST':
        selected_test_ids = request.POST.getlist('test')
        verdict = "Пригоден" if not selected_test_ids else "Не пригоден"
        return render(request, 'core/defects.html', {
            'inventories': inventories,
            'groups': groups,
            'objects': objects,
            'tests': tests,
            'verdict': verdict,
            'selected_inventory_id': int(selected_inventory_id) if selected_inventory_id else None,
            'selected_group_id': int(selected_group_id) if selected_group_id else None,
            'selected_object_id': int(selected_object_id) if selected_object_id else None,
        })

    return render(request, 'core/defects.html', {
        'inventories': inventories,
        'groups': groups,
        'objects': objects,
        'tests': tests,
        'verdict': verdict,
        'selected_inventory_id': int(selected_inventory_id) if selected_inventory_id else None,
        'selected_group_id': int(selected_group_id) if selected_group_id else None,
        'selected_object_id': int(selected_object_id) if selected_object_id else None,
    })