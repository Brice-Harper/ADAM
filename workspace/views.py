from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, date
from urllib.parse import urlencode
from .models import Note, Log
from .forms import NoteForm
from .utils import log_action


def index(request):
    from tasks.models import Task

    total_notes = Note.objects.filter(author=request.user).count()
    recent_notes = Note.objects.filter(author=request.user).order_by("-updated_at")[:3]

    from django.utils import timezone
    from datetime import timedelta

    une_semaine = timezone.now() - timedelta(days=7)
    notes_semaine = Note.objects.filter(
        author=request.user, created_at__gte=une_semaine
    ).count()

    total_tasks = Task.objects.filter(author=request.user).count()
    tasks_done = Task.objects.filter(author=request.user, status="done").count()
    tasks_urgent = Task.objects.filter(
        author=request.user, priority="urgent", status__in=["todo", "in_progress"]
    ).count()

    context = {
        "is_workspace": True,
        "total_notes": total_notes,
        "recent_notes": recent_notes,
        "notes_semaine": notes_semaine,
        "total_tasks": total_tasks,
        "tasks_done": tasks_done,
        "tasks_urgent": tasks_urgent,
    }
    return render(request, "workspace/index.html", context)


def note_list(request):
    query = request.GET.get("q", "")
    notes_queryset = Note.objects.filter(author=request.user).order_by("-updated_at")

    if query:
        notes_queryset = notes_queryset.filter(title__icontains=query)

    paginator = Paginator(notes_queryset, 10)
    page_number = request.GET.get("page")
    notes = paginator.get_page(page_number)

    context = {
        "is_workspace": True,
        "notes": notes,
        "query": query,
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
            log_action(request.user, "note_create", note.title)
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
            log_action(request.user, "note_update", note.title)
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
        log_action(request.user, "note_delete", note.title)
        note.delete()
        messages.success(request, "Note supprimée avec succès")
        return redirect("note_list")

    context = {
        "is_workspace": True,
        "note": note,
    }
    return render(request, "workspace/note_confirm_delete.html", context)


def log_list(request):
    logs_queryset = Log.objects.all().order_by("-created_at")

    # Filtre par action
    action_filter = request.GET.get("action", "")
    if action_filter:
        logs_queryset = logs_queryset.filter(action=action_filter)

    # Filtre par période
    periode_filter = request.GET.get("periode", "")
    if periode_filter:
        if periode_filter == "today":
            debut = timezone.now().replace(hour=0, minute=0, second=0)
        elif periode_filter == "week":
            debut = timezone.now() - timedelta(days=7)
        elif periode_filter == "month":
            debut = timezone.now() - timedelta(days=30)
        logs_queryset = logs_queryset.filter(created_at__gte=debut)

    # Pagination
    paginator = Paginator(logs_queryset, 50)
    page_number = request.GET.get("page")
    logs = paginator.get_page(page_number)

    # Statistiques
    stats = Log.objects.values("action").annotate(total=Count("id")).order_by("-total")

    # Données du graphique - activité des 30 derniers jours
    aujourd_hui = timezone.now().date()
    trente_jours = [aujourd_hui - timedelta(days=i) for i in range(29, -1, -1)]

    logs_30_jours = (
        Log.objects.filter(created_at__date__gte=aujourd_hui - timedelta(days=29))
        .values("created_at__date")
        .annotate(total=Count("id"))
    )

    logs_par_jour = {
        entry["created_at__date"]: entry["total"] for entry in logs_30_jours
    }

    graphique_labels = [jour.strftime("%d/%m") for jour in trente_jours]
    graphique_data = [logs_par_jour.get(jour, 0) for jour in trente_jours]

    context = {
        "is_workspace": True,
        "logs": logs,
        "stats": stats,
        "action_filter": action_filter,
        "periode_filter": periode_filter,
        "action_choices": Log.ACTION_CHOICES,
        "graphique_labels": graphique_labels,
        "graphique_data": graphique_data,
    }
    return render(request, "workspace/log_list.html", context)
