from django.urls import path
from . import views

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("create/", views.article_create, name="article_create"),
    path("<int:article_id>/update/", views.article_update, name="article_update"),
    path("<int:article_id>/delete/", views.article_delete, name="article_delete"),
    path("<int:article_id>/preview/", views.article_preview, name="article_preview"),
    path("categories/", views.blog_category_list, name="blog_category_list"),
    path(
        "categories/<int:category_id>/delete/",
        views.blog_category_delete,
        name="blog_category_delete",
    ),
    path("tags/", views.blog_tag_list, name="blog_tag_list"),
    path("tags/<int:tag_id>/delete/", views.blog_tag_delete, name="blog_tag_delete"),
]
