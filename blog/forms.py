from django import forms
from django_quill.forms import QuillFormField
from .models import Article, Category, Tag


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "color"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "input", "placeholder": "Nom de la catégorie"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "textarea", "placeholder": "Description (optionnel)", "rows": 2}
        )
        self.fields["color"].widget = forms.TextInput(
            attrs={
                "type": "color",
                "class": "color-picker",
            }
        )


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "input", "placeholder": "Nom du tag"}
        )


class ArticleForm(forms.ModelForm):
    content = QuillFormField()

    class Meta:
        model = Article
        fields = [
            "title",
            "excerpt",
            "content",
            "cover_image",
            "cover_image_url",
            "category",
            "tags",
            "status",
            "seo_title",
            "seo_description",
            "seo_keywords",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update(
            {"class": "input", "placeholder": "Titre de l'article"}
        )
        self.fields["excerpt"].widget.attrs.update(
            {
                "class": "textarea",
                "placeholder": "Résumé court affiché dans la liste des articles",
                "rows": 3,
            }
        )
        self.fields["cover_image"].widget.attrs.update(
            {
                "class": "input",
            }
        )
        self.fields["cover_image_url"].widget.attrs.update(
            {"class": "input", "placeholder": "https://exemple.com/image.jpg"}
        )
        self.fields["cover_image_url"].required = False
        self.fields["excerpt"].required = False
        self.fields["status"].widget.attrs.update({"class": "select"})
        self.fields["category"].required = False
        self.fields["category"].widget.attrs.update({"class": "select"})
        self.fields["tags"].required = False
        self.fields["tags"].widget.attrs.update({"class": "select"})
        self.fields["seo_title"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Titre SEO (60 caractères max)",
                "maxlength": "60",
            }
        )
        self.fields["seo_description"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Description SEO (160 caractères max)",
                "maxlength": "160",
            }
        )
        self.fields["seo_keywords"].widget.attrs.update(
            {"class": "input", "placeholder": "mot-clé1, mot-clé2, mot-clé3"}
        )
