from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField


class Collection(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    color = models.CharField(max_length=7, default="#4f6bdc", verbose_name="Couleur")
    icon = models.CharField(max_length=50, default="fa-folder", verbose_name="Icône")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def bookmark_count(self):
        return self.bookmarks.count()


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    url = models.URLField(max_length=2000, verbose_name="URL")
    title = models.CharField(max_length=500, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.URLField(max_length=2000, blank=True, verbose_name="Image")
    notes = QuillField(blank=True, null=True, verbose_name="Notes personnelles")
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookmarks",
        verbose_name="Collection",
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
