from django.urls import path
from . import views

urlpatterns = [
    path("", views.bookmark_list, name="bookmark_list"),
    path("create/", views.bookmark_create, name="bookmark_create"),
    path("<int:bookmark_id>/", views.bookmark_detail, name="bookmark_detail"),
    path("<int:bookmark_id>/update/", views.bookmark_update, name="bookmark_update"),
    path("<int:bookmark_id>/delete/", views.bookmark_delete, name="bookmark_delete"),
    path("fetch-metadata/", views.fetch_metadata_view, name="fetch_metadata"),
    path("collections/", views.collection_list, name="collection_list"),
    path(
        "collections/<int:collection_id>/",
        views.collection_detail,
        name="collection_detail",
    ),
    path(
        "collections/<int:collection_id>/update/",
        views.collection_update,
        name="collection_update",
    ),
    path(
        "collections/<int:collection_id>/delete/",
        views.collection_delete,
        name="collection_delete",
    ),
    path("tags/", views.tag_list, name="tag_list"),
    path("tags/<int:tag_id>/delete/", views.tag_delete, name="tag_delete"),
]
