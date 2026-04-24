from django import forms
from django_quill.fields import QuillFormField
from .models import Task, SubTask, Category, Label


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "color"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "input", "placeholder": "Nom de la catégorie"}
        )
        self.fields["color"].widget = forms.TextInput(
            attrs={"class": "color-picker", "type": "color"}
        )


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name", "color"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "input", "placeholder": "Nom de l'étiquette"}
        )
        self.fields["color"].widget = forms.TextInput(
            attrs={"class": "color-picker", "type": "color"}
        )


class TaskForm(forms.ModelForm):
    description = QuillFormField(required=False)

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category",
            "labels",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update(
            {"class": "input", "placeholder": "Titre de la tâche"}
        )
        self.fields["priority"].widget.attrs.update({"class": "select"})
        self.fields["status"].widget.attrs.update({"class": "select"})
        self.fields["due_date"].widget = forms.DateInput(
            attrs={"class": "input", "type": "date"}
        )
        self.fields["due_date"].required = False

        if user:
            self.fields["category"].queryset = Category.objects.filter(author=user)
            self.fields["labels"].queryset = Label.objects.filter(author=user)

        self.fields["category"].required = False
        self.fields["category"].widget.attrs.update({"class": "select"})
        self.fields["labels"].required = False
        self.fields["labels"].widget.attrs.update({"class": "select"})


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "input", "placeholder": "Titre de la sous-tâche"}
        )
