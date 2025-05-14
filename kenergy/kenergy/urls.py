from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка Django
    path('', include('core.urls')),   # Маршруты приложения core
]