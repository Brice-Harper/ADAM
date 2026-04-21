from django.contrib import admin
from .models import Note, Log


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ["created_at", "user", "action", "detail"]
    list_filter = ["action", "user"]
    search_fields = ["deteil", "user__username"]
    readonly_fields = ["user", "action", "detail", "created_at"]
    ordering = ["-created_at"]
