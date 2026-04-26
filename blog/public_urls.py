from django.urls import path
from . import public_views

urlpatterns = [
    path("", public_views.blog_home, name="blog_home"),
    path("article/<slug:slug>/", public_views.article_detail, name="article_detail"),
    path("categorie/<slug:slug>/", public_views.blog_category, name="blog_category"),
    path("tag/<slug:slug>/", public_views.blog_tag, name="blog_tag"),
]
