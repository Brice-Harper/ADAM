from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from .models import Note
from .forms import NoteForm


def index(request):
    context = {
        "is_workspace": True,
    }
    return render(request, "workspace/index.html", context)


def note_list(request):
    notes = Note.objects.filter(author=request.user).order_by("-updated_at")
    context = {
        "is_workspace": True,
        "notes": notes,
    }
    return render(request, "workspace/note_list.html", context)


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, author=request.user)
    context = {
        "is_workspace": True,
        "note": note,
    }
    return render(request, "workspace/note_detail.html", context)


def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            messages.success(request, "Note créée avec succès")
            url = reverse("note_list") + "?" + urlencode({"highlight": note.id})
            return redirect(url)
    else:
        form = NoteForm()

    context = {
        "is_workspace": True,
        "form": form,
        "page_title": "Créer une nouvelle note",
        "submit_label": "Créer",
    }
    return render(request, "workspace/note_form.html", context)


def note_update(request, note_id):
    note = get_object_or_404(Note, id=note_id, author=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note mise à jour avec succès")
            url = reverse("note_list") + "?" + urlencode({"highlight": note.id})
            return redirect(url)
    else:
        form = NoteForm(instance=note)

    context = {
        "is_workspace": True,
        "form": form,
        "page_title": "Modifier la note",
        "submit_label": "Mettre à jour",
    }
    return render(request, "workspace/note_form.html", context)


def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id, author=request.user)

    if request.method == "POST":
        note.delete()
        messages.success(request, "Note supprimée avec succès")
        return redirect("note_list")

    context = {
        "is_workspace": True,
        "note": note,
    }
    return render(request, "workspace/note_confirm_delete.html", context)
