from django.contrib import admin
from .models import Collection, Tag, Bookmark


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name", "color", "icon", "author", "bookmark_count"]
    search_fields = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "author"]
    search_fields = ["name"]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "collection", "author", "created_at"]
    list_filter = ["collection"]
    search_fields = ["title", "url", "description"]
    filter_horizontal = ["tags"]
