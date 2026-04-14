from django.shortcuts import render, get_object_or_404
from .models import Note


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
