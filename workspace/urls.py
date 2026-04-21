from django.urls import path
from .views import (
    index,
    note_list,
    note_detail,
    note_create,
    note_update,
    note_delete,
    log_list,
)


urlpatterns = [
    path("", index, name="workspace_index"),
    path("notes/", note_list, name="note_list"),
    path("notes/create/", note_create, name="note_create"),
    path("notes/<int:note_id>/", note_detail, name="note_detail"),
    path("notes/<int:note_id>/update/", note_update, name="note_update"),
    path("notes/<int:note_id>/delete/", note_delete, name="note_delete"),
    path("logs/", log_list, name="log_list"),
]
