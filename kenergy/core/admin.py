from django.contrib import admin
from .models import Inventory, Groups, Object, Tests, Standards

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id_i', 'название')

@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('id_g', 'id_i', 'название')

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('id_o', 'id_g', 'название')

@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    list_display = ('id_def', 'id_o', 'испытание', 'метрика', 'рекомендация')

@admin.register(Standards)
class StandardsAdmin(admin.ModelAdmin):
    list_display = ('id_s', 'id_o', 'стандарт', 'требование')