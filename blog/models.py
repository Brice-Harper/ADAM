from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_quill.fields import QuillField
import unicodedata
import re


def slugify_fr(text):
    """
    Génère un slug propre depuis un texte français.
    Gère les accents et caractères spéciaux.
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    color = models.CharField(max_length=7, default="#4f6bdc", verbose_name="Couleur")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_fr(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_fr(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):

    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("published", "Publié"),
        ("archived", "Archivé"),
    ]

    # Contenu principal
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    excerpt = models.TextField(
        blank=True,
        verbose_name="Extrait",
        help_text="Résumé court affiché dans la liste des articles",
    )
    content = QuillField(verbose_name="Contenu")

    # Image de couverture
    cover_image = models.ImageField(
        upload_to="blog/covers/",
        blank=True,
        null=True,
        verbose_name="Image de couverture (upload)",
    )
    cover_image_url = models.URLField(
        max_length=2000, blank=True, verbose_name="Image de couverture (URL externe)"
    )

    # Organisation
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name="Catégorie",
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")

    # Statut et dates
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft", verbose_name="Statut"
    )
    published_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Date de publication"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification"
    )

    # Auteur
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="Auteur"
    )

    # SEO
    seo_title = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Titre SEO",
        help_text="60 caractères maximum recommandés",
    )
    seo_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Description SEO",
        help_text="160 caractères maximum recommandés",
    )
    seo_keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Mots-clés SEO",
        help_text="Séparés par des virgules",
    )

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Générer le slug automatiquement depuis le titre
        if not self.slug:
            base_slug = slugify_fr(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Enregistrer la date de publication quand on publie
        if self.status == "published" and not self.published_at:
            from django.utils import timezone

            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_cover_image(self):
        """Retourne l'URL de l'image de couverture (upload ou URL externe)."""
        if self.cover_image:
            return self.cover_image.url
        return self.cover_image_url or ""

    def reading_time(self):
        """Estime le temps de lecture en minutes (250 mots/minute)."""
        if self.content:
            word_count = len(str(self.content).split())
            minutes = max(1, round(word_count / 250))
            return minutes
        return 1
