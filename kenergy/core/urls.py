from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_db/', views.edit_db, name='edit_db'),
    path('system_settings/', views.system_settings, name='system_settings'),
    path('regulations/', views.regulations, name='regulations'),
    path('definition/', views.definition, name='definition'),
    path('defects/', views.defects, name='defects'),
]