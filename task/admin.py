from django.contrib import admin
from django.db.models import Sum, Count

from .models import Project, Task, Department, Role


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'manager')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'executor')


class RoleInLine(admin.TabularInline):
    model = Role


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [RoleInLine]
    list_display = ('name', 'id', 'description')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'is_header', 'is_manager')
    list_filter = ('department', 'is_header', 'is_manager')
