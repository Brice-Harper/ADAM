from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField


class Note(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
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


class Log(models.Model):

    ACTION_CHOICES = [
        ("login", "Connexion"),
        ("logout", "Déconnexion"),
        ("note_create", "Création de note"),
        ("note_update", "Modification de note"),
        ("note_delete", "Suppression de note"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Utilisateur",
    )
    action = models.CharField(
        max_length=50, choices=ACTION_CHOICES, verbose_name="Action"
    )
    detail = models.CharField(max_length=255, blank=True, verbose_name="Détail")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.created_at}"
