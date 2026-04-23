from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("create/", views.task_create, name="task_create"),
    path("<int:task_id>/", views.task_detail, name="task_detail"),
    path("<int:task_id>/update/", views.task_update, name="task_update"),
    path("<int:task_id>/delete/", views.task_delete, name="task_delete"),
    path("<int:task_id>/toggle/", views.task_toggle, name="task_toggle"),
    path("reorder/", views.task_reorder, name="task_reorder"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path(
        "categories/<int:category_id>/delete/",
        views.category_delete,
        name="category_delete",
    ),
    path("labels/", views.label_list, name="label_list"),
    path("labels/create/", views.label_create, name="label_create"),
    path("labels/<int:label_id>/delete/", views.label_delete, name="label_delete"),
]
