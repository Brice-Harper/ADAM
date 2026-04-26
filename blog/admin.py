from django.contrib import admin
from .models import Category, Tag, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "color"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "category", "author", "published_at"]
    list_filter = ["status", "category"]
    search_fields = ["title", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    readonly_fields = ["published_at", "created_at", "updated_at"]
    fieldsets = [
        ("Contenu", {"fields": ["title", "slug", "excerpt", "content"]}),
        ("Image de couverture", {"fields": ["cover_image", "cover_image_url"]}),
        ("Organisation", {"fields": ["category", "tags"]}),
        (
            "Publication",
            {
                "fields": [
                    "status",
                    "author",
                    "published_at",
                    "created_at",
                    "updated_at",
                ]
            },
        ),
        (
            "SEO",
            {
                "fields": ["seo_title", "seo_description", "seo_keywords"],
                "classes": ["collapse"],
            },
        ),
    ]
