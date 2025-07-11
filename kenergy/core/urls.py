"""kenergy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# core/urls.py
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [

    path('api/groups/', views.get_groups, name='get_groups'),
    path('api/objects/', views.get_objects, name='get_objects'),
    path('', views.login_view, name='login'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('edit-db/', views.edit_db, name='edit_db'),
    path('save-object/', views.save_object, name='save_object'),
    path('system-settings/', views.system_settings, name='system_settings'),
    path('regulations/', views.regulations, name='regulations'),
    path('definition/', views.definition, name='definition'),
    path('defects/', views.defects, name='defects'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Инвентарь
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/create/', views.inventory_create, name='inventory_create'),
    # path('inventory/edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),
    # path('inventory/delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),

    path('inventory/edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),
    path('groups/edit/<int:pk>/', views.groups_edit, name='groups_edit'),
    path('object/edit/<int:pk>/', views.object_edit, name='object_edit'),

    path('inventory/delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),
    path('groups/delete/<int:pk>/', views.groups_delete, name='groups_delete'),
    path('object/delete/<int:pk>/', views.object_delete, name='object_delete'),
    # Группы
    path('groups/', views.groups_list, name='groups_list'),
    path('groups/create/', views.groups_create, name='groups_create'),
    # path('groups/edit/<int:pk>/', views.groups_edit, name='groups_edit'),
    # path('groups/delete/<int:pk>/', views.groups_delete, name='groups_delete'),

    # Объекты
    path('object/', views.object_list, name='object_list'),
    path('object/create/', views.object_create, name='object_create'),
    # path('object/edit/<int:pk>/', views.object_edit, name='object_edit'),
    # path('object/delete/<int:pk>/', views.object_delete, name='object_delete'),

    # Тесты
    # path('tests/', views.tests_list, name='tests_list'),
    # path('tests/create/', views.tests_create, name='tests_create'),
    # path('tests/edit/<int:pk>/', views.tests_edit, name='tests_edit'),
    # path('tests/delete/<int:pk>/', views.tests_delete, name='tests_delete'),

    # Стандарты
    # path('standards/', views.standards_list, name='standards_list'),
    # path('standards/create/', views.standards_create, name='standards_create'),
    # path('standards/edit/<int:pk>/', views.standards_edit, name='standards_edit'),
    # path('standards/delete/<int:pk>/', views.standards_delete, name='standards_delete'),
    path('update-row/', views.update_row, name='update_row'),
    path('delete-row/', views.delete_row, name='delete_row'),
    path('save-new-row/', views.save_new_row, name='save_new_row'),
    path('api/regulations/', views.get_regulations, name='get_regulations'),
    path('api/defects/', views.get_defects, name='get_defects'),
]
