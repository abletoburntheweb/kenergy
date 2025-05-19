from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),  # Страница авторизации
    path('', views.admin_panel, name='admin_panel'),  # Административная панель
    path('add_user/', views.add_user, name='add_user'),  # Добавление пользователя
    path('edit_db/', views.edit_db, name='edit_db'),  # Редактирование БД
    path('view_users/', views.view_users, name='view_users'),  # Просмотр пользователей
    path('add_object/', views.add_object, name='add_object'),  # Добавление объекта
    path('system_settings/', views.system_settings, name='system_settings'),  # Настройки системы
    path('regulations/', views.regulations, name='regulations'),  # Положения
    path('definition/', views.definition, name='definition'),  # Определение объекта
    path('defects/', views.defects, name='defects'),  # Дефекты
]