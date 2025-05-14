from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),      # Страница авторизации
    path('register/', views.register, name='register'),  # Страница регистрации
    path('home/', views.home, name='home'),              # Главная страница
    path('add_user/', views.add_user, name='add_user'),  # Страница добавления пользователей
]