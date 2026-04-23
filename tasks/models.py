from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    color = models.CharField(max_length=7, default="#4f6bdc", verbose_name="Couleur")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    color = models.CharField(max_length=7, default="#48c774", verbose_name="Couleur")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")

    class Meta:
        verbose_name = "Étiquette"
        verbose_name_plural = "Étiquettes"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):

    PRIORITY_CHOICES = [
        ("low", "Basse"),
        ("normal", "Normale"),
        ("high", "Haute"),
        ("urgent", "Urgente"),
    ]

    STATUS_CHOICES = [
        ("todo", "À faire"),
        ("in_progress", "En cours"),
        ("done", "Terminée"),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    description = QuillField(blank=True, null=True, verbose_name="Description")
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="normal",
        verbose_name="Priorité",
    )
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="todo", verbose_name="Statut"
    )
    due_date = models.DateField(null=True, blank=True, verbose_name="Date d'échéance")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Catégorie",
    )
    labels = models.ManyToManyField(Label, blank=True, verbose_name="Étiquettes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"
        ordering = ["order", "-priority", "due_date"]

    def __str__(self):
        return self.title


class SubTask(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
        verbose_name="Tâche parente",
    )
    title = models.CharField(max_length=200, verbose_name="Titre")
    is_done = models.BooleanField(default=False, verbose_name="Terminée")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Sous-tâche"
        verbose_name_plural = "Sous-tâches"
        ordering = ["order"]

    def __str__(self):
        return self.title
