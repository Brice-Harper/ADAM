from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField


class Note(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    content = models.TextField(verbose_name="Contenu")
    content_rich = QuillField(blank=True, null=True, verbose_name="Contenu enrichi")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title
