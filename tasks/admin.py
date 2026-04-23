from django.contrib import admin
from .models import Category, Label, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "color", "author"]
    search_fields = ["name"]


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ["name", "color", "author"]
    search_fields = ["name"]


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ["title", "is_done", "order"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "priority", "category", "due_date", "author"]
    list_filter = ["status", "priority", "category"]
    search_fields = ["title", "description"]
    filter_horizontal = ["labels"]
    inlines = [SubTaskInline]


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ["title", "task", "is_done", "order"]
    list_filter = ["is_done"]
