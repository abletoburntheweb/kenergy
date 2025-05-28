# core/views.py
import json
import sys
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Inventory, Groups as GroupsModel, Object, Tests, Standards, Groups
from .user import (
    UserInventoryForm,
    UserGroupForm,
    UserObjectForm,
    UserTestsForm,
    UserStandardsForm,
)

logger = logging.getLogger(__name__)
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
            return JsonResponse({
                'success': True,
                'id': form.instance.id_i,
                'name': form.instance.название
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@login_required
def inventory_edit(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = UserInventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'id': inventory.id_i,
                'name': inventory.название
            })
        else:
            logger.error(f"Validation errors in UserInventoryForm: {form.errors}")
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors)
            }, status=400)
    else:
        form = UserInventoryForm(instance=inventory)
    return render(request, 'core/inventory_edit.html', {'form': form})

@csrf_exempt
@login_required
def inventory_delete(request, pk):
    try:
        inventory = Inventory.objects.get(pk=pk)
        inventory.delete()
        return JsonResponse({'success': True})
    except Inventory.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Инвентарь не найден.'}, status=404)


@login_required
def groups_list(request):
    inventory_id = request.GET.get('inventory')
    if inventory_id:
        try:
            inventory = Inventory.objects.get(id_i=inventory_id)
            groups = GroupsModel.objects.filter(inventory=inventory).values('id_g', 'name')
            return JsonResponse(list(groups), safe=False)
        except Inventory.DoesNotExist:
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)


def groups_create(request):
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id')
        name = request.POST.get('name')
        logger.debug(f"Received POST data: inventory_id={inventory_id}, name={name}")

        # Добавьте логирование для каждого шага
        try:
            inventory = Inventory.objects.get(id_i=inventory_id)
            logger.info(f"Инвентарь найден: id_i={inventory_id}")
        except Inventory.DoesNotExist:
            logger.error(f"Inventory с id_i={inventory_id} не найден.")
            return JsonResponse(
                {'success': False, 'message': f'Inventory с id_i={inventory_id} не найден.'},
                status=404
            )

        if Groups.objects.filter(id_i=inventory, название=name).exists():
            logger.warning(f"Группа с именем '{name}' уже существует для Inventory с id_i={inventory_id}.")
            return JsonResponse(
                {'success': False, 'message': f'Группа с именем "{name}" уже существует.'},
                status=400
            )

        try:
            group = Groups.objects.create(id_i=inventory, название=name)
            logger.info(f"Группа успешно создана: id_g={group.id_g}, название={name}")
            return JsonResponse(
                {
                    'success': True,
                    'message': 'Группа успешно создана.',
                    'id_g': group.id_g,
                    'название': group.название
                },
                status=201
            )
        except Exception as e:
            logger.error(f"Ошибка при создании группы: {e}")
            return JsonResponse(
                {'success': False, 'message': f'Ошибка при создании группы: {e}'},
                status=500
            )
    else:
        logger.error("Неверный метод запроса.")
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса.'}, status=405)

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

@csrf_exempt
@login_required
def groups_delete(request, pk):
    try:
        group = Groups.objects.get(pk=pk)
        group.delete()
        return JsonResponse({'success': True})
    except Groups.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Группа не найдена.'}, status=404)


@login_required
def object_list(request):
    objects = Object.objects.all()
    return render(request, 'core/object_list.html', {'objects': objects})

@login_required
def object_create(request):
    if request.method == 'POST':
        form = UserObjectForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({
                'success': True,
                'id': obj.id_o,
                'name': obj.название
            })
        else:
            logger.error(f"Validation errors in UserObjectForm: {form.errors}")
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors)
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

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

@csrf_exempt
@login_required
def object_delete(request, pk):
    try:
        obj = Object.objects.get(pk=pk)
        obj.delete()
        return JsonResponse({'success': True})
    except Object.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Объект не найден.'}, status=404)

@login_required
def defects_list(request):
    defects = Tests.objects.all()
    return render(request, 'core/defects_list.html', {'defects': defects})

@login_required
def defects_create(request):
    if request.method == 'POST':
        form = UserTestsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('defects_list')
    else:
        form = UserTestsForm()
    return render(request, 'core/defects_form.html', {'form': form})

@login_required
def defects_edit(request, pk):
    defect = get_object_or_404(Tests, pk=pk)
    if request.method == 'POST':
        form = UserTestsForm(request.POST, instance=defect)
        if form.is_valid():
            form.save()
            return redirect('defects_list')
    else:
        form = UserTestsForm(instance=defect)
    return render(request, 'core/defects_form.html', {'form': form})

@login_required
def defects_delete(request, pk):
    defect = get_object_or_404(Tests, pk=pk)
    if request.method == 'POST':
        defect.delete()
        return redirect('defects_list')
    return render(request, 'core/defects_confirm_delete.html', {'defect': defect})

@login_required
def standards_list(request):
    standards = Standards.objects.all()
    return render(request, 'core/standards_list.html', {'standards': standards})

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
    logger.debug(f"Inventory ID: {inventory_id}")
    if not inventory_id:
        return JsonResponse([], safe=False)
    groups = GroupsModel.objects.filter(id_i=inventory_id).values('id_g', 'название')
    logger.debug(f"Groups: {list(groups)}")
    return JsonResponse(list(groups), safe=False)
def get_objects(request):
    group_id = request.GET.get('group')
    objects = Object.objects.filter(id_g=group_id).values('id_o', 'название')
    return JsonResponse(list(objects), safe=False)
@login_required
def system_settings(request):
    return render(request, 'core/system_settings.html')

@login_required
def save_object(request):
    logger.debug("Запрос POST в save_object получен.")
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory')
        group_id = request.POST.get('group')
        object_id = request.POST.get('object')
        standards = request.POST.getlist('standard[]')
        requirements = request.POST.getlist('requirement[]')
        defects = request.POST.getlist('defect[]')
        recommendations = request.POST.getlist('recommendation[]')
        metrics = request.POST.getlist('metric[]')

        if not inventory_id or not group_id:
            logger.error("Inventory или Group не выбраны.")
            return JsonResponse({'success': False, 'message': 'Inventory или Group не выбраны.'}, status=400)

        try:
            inventory = Inventory.objects.get(id_i=inventory_id)
            group = GroupsModel.objects.get(id_g=group_id)
        except (Inventory.DoesNotExist, GroupsModel.DoesNotExist) as e:
            logger.error(f"Ошибка при получении Inventory или Group: {e}")
            return JsonResponse({'success': False, 'message': f'Ошибка при получении Inventory или Group: {e}'}, status=400)

        if object_id:
            obj = Object.objects.get(id_o=object_id)
            obj.id_g = group
            obj.save()
        else:
            obj = Object.objects.create(id_g=group, название="Новый объект")

        for standard, requirement in zip(standards, requirements):
            existing_standard = Standards.objects.filter(id_o=obj, стандарт=standard, требование=requirement).first()
            if not existing_standard:
                Standards.objects.create(id_o=obj, стандарт=standard, требование=requirement)

        for defect, recommendation, metric in zip(defects, recommendations, metrics):
            existing_defect = Tests.objects.filter(id_o=obj, испытание=defect, рекомендация=recommendation, метрика=float(metric)).first()
            if not existing_defect:
                Tests.objects.create(
                    id_o=obj,
                    испытание=defect,
                    рекомендация=recommendation,
                    метрика=float(metric)
                )

        logger.debug("Данные успешно сохранены.")
        return JsonResponse({'success': True, 'message': 'Данные успешно сохранены.'})

    logger.error("Неверный метод запроса.")
    return JsonResponse({'success': False, 'message': 'Неверный метод запроса.'}, status=405)

@login_required
def save_new_row(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            object_id = data.get('object_id')
            table = data.get('table')
            row_data = data.get('data')

            obj = Object.objects.get(id_o=object_id)

            if table == 'regulations-table':
                standard = Standards.objects.create(
                    id_o=obj,
                    стандарт=row_data.get('standard'),
                    требование=row_data.get('requirement')
                )
                return JsonResponse({'success': True, 'id': standard.id_s})
            elif table == 'defects-table':
                defect = Tests.objects.create(
                    id_o=obj,
                    испытание=row_data.get('defect'),
                    рекомендация=row_data.get('recommendation'),
                    метрика=row_data.get('metric')
                )
                return JsonResponse({'success': True, 'id': defect.id_def})

        except Exception as e:
            logger.error(f"Ошибка при сохранении новой строки: {e}")
            return JsonResponse({'success': False, 'message': 'Произошла ошибка при сохранении данных.'}, status=500)

    return JsonResponse({'success': False, 'message': 'Неверный метод запроса.'}, status=405)

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
        groups = GroupsModel.objects.filter(id_i=selected_inventory)

    if selected_group:
        objects = Object.objects.filter(id_g=selected_group)

    if selected_object:
        standards = Standards.objects.filter(id_o=selected_object)
    else:
        standards = []

    if request.method == 'POST' and 'continue_button' in request.POST:
        show_requirements = True

        completed_ids = request.POST.getlist('standard_checkbox')

        if selected_object:
            if not completed_ids:
                unmet_requirements = standards
            else:
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
    groups = GroupsModel.objects.filter(id_i=selected_inventory_id) if selected_inventory_id else []

    selected_group_id = request.GET.get('group')
    defects = Tests.objects.filter(id_o__id_g=selected_group_id).select_related('id_o') if selected_group_id else []

    selected_defect_ids = request.GET.getlist('defect')
    objects = Object.objects.filter(defects__id_def__in=selected_defect_ids).distinct() if selected_defect_ids else []

    verdict = None
    if request.method == 'POST':
        selected_defect_ids = request.POST.getlist('defect')
        objects = Object.objects.filter(defects__id_def__in=selected_defect_ids).distinct()
        verdict = "Объект определен." if objects else "Не удалось определить объект."

    return render(request, 'core/definition.html', {
        'inventories': inventories,
        'groups': groups,
        'defects': defects,
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
                if abs(entered_value_float - test.метрика) > 1e-9:
                    discrepancies.append(test)
                    recommendations[test.id_def] = test.рекомендация
            except (ValueError, TypeError):
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
@login_required
def get_regulations(request):
    object_id = request.GET.get('object')
    if not object_id:
        return JsonResponse([], safe=False)
    regulations = Standards.objects.filter(id_o=object_id).values('id_s', 'стандарт', 'требование')
    return JsonResponse(list(regulations), safe=False)

@login_required
def get_defects(request):
    object_id = request.GET.get('object')
    if not object_id:
        return JsonResponse([], safe=False)
    defects = Tests.objects.filter(id_o=object_id).values('id_def', 'испытание', 'рекомендация', 'метрика')
    return JsonResponse(list(defects), safe=False)

@login_required
def update_row(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            object_id = data.get('object_id')
            table = data.get('table')
            row_data = data.get('data')

            row_id = row_data.get('id')
            if not row_id:
                return JsonResponse({'success': False, 'message': 'Уникальный идентификатор строки отсутствует.'}, status=400)

            if table == 'regulations-table':
                standard = row_data.get('standard')
                requirement = row_data.get('requirement')
                Standards.objects.filter(id_o=object_id, id_s=row_id).update(
                    стандарт=standard,
                    требование=requirement
                )
            elif table == 'defects-table':
                defect = row_data.get('defect')
                recommendation = row_data.get('recommendation')
                metric = row_data.get('metric')
                Tests.objects.filter(id_o=object_id, id_def=row_id).update(
                    испытание=defect,
                    рекомендация=recommendation,
                    метрика=metric
                )

            return JsonResponse({'success': True, 'message': 'Данные успешно обновлены.'})
        except Exception as e:
            logger.error(f"Ошибка при обновлении строки: {e}")
            return JsonResponse({'success': False, 'message': 'Произошла ошибка при обновлении данных.'}, status=500)

    return JsonResponse({'success': False, 'message': 'Неверный метод запроса.'}, status=405)

@login_required
def delete_row(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            object_id = data.get('object_id')
            table = data.get('table')
            row_data = data.get('data')

            if table == 'regulations-table':
                standard = row_data.get('standard')
                requirement = row_data.get('requirement')
                Standards.objects.filter(id_o=object_id, стандарт=standard, требование=requirement).delete()
            elif table == 'defects-table':
                defect = row_data.get('defect')
                recommendation = row_data.get('recommendation')
                metric = row_data.get('metric')
                Tests.objects.filter(id_o=object_id, испытание=defect, рекомендация=recommendation, метрика=metric).delete()

            return JsonResponse({'success': True, 'message': 'Данные успешно удалены.'})
        except Exception as e:
            logger.error(f"Ошибка при удалении строки: {e}")
            return JsonResponse({'success': False, 'message': 'Произошла ошибка при удалении данных.'}, status=500)

    return JsonResponse({'success': False, 'message': 'Неверный метод запроса.'}, status=405)