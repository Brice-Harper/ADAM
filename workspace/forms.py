import json
from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update(
            {"class": "input", "placeholder": "Titre de la note"}
        )
        self.fields["content"].widget.attrs.update(
            {"class": "input", "placeholder": "Contenu de la note"}
        )
