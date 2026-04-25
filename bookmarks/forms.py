from django import forms
from django_quill.forms import QuillFormField
from .models import Bookmark, Collection, Tag


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "description", "color", "icon"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "input", "placeholder": "Nom de la collection"}
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
        self.fields["icon"].widget.attrs.update(
            {"class": "input", "placeholder": "fa-folder"}
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


class BookmarkForm(forms.ModelForm):
    notes = QuillFormField(required=False)

    class Meta:
        model = Bookmark
        fields = ["url", "title", "description", "image", "notes", "collection", "tags"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["url"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "https://...",
                "id": "bookmark-url",
            }
        )
        self.fields["title"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Titre de la page",
                "id": "bookmark-title",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "textarea",
                "placeholder": "Description",
                "rows": 2,
                "id": "bookmark-description",
            }
        )
        self.fields["image"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "URL de l'image (optionnel)",
                "id": "bookmark-image",
            }
        )
        self.fields["image"].required = False
        self.fields["description"].required = False

        if user:
            self.fields["collection"].queryset = Collection.objects.filter(author=user)
            self.fields["tags"].queryset = Tag.objects.filter(author=user)

        self.fields["collection"].required = False
        self.fields["collection"].widget.attrs.update({"class": "select"})
        self.fields["tags"].required = False
        self.fields["tags"].widget.attrs.update({"class": "select"})
