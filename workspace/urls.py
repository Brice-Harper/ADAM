from django.urls import path
from .views import index, note_list, note_detail


urlpatterns = [
    path("", index, name="workspace_index"),
    path("notes/", note_list, name="note_list"),
    path("notes/<int:note_id>/", note_detail, name="note_detail"),
]
