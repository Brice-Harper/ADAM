from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
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
    from bookmarks.models import Bookmark
    from blog.models import Article
    from django.utils import timezone
    from datetime import timedelta, date
    from django.db.models import Count

    aujourd_hui = date.today()
    une_semaine = timezone.now() - timedelta(days=7)
    trente_jours = timezone.now() - timedelta(days=30)

    # Notes
    total_notes = Note.objects.filter(author=request.user).count()
    notes_semaine = Note.objects.filter(
        author=request.user, created_at__gte=une_semaine
    ).count()
    recent_notes = Note.objects.filter(author=request.user).order_by("-updated_at")[:3]

    # Tâches
    total_tasks = Task.objects.filter(author=request.user).count()
    tasks_urgent = Task.objects.filter(
        author=request.user, priority="urgent", status__in=["todo", "in_progress"]
    ).count()
    tasks_aujourd_hui = Task.objects.filter(
        author=request.user, due_date=aujourd_hui, status__in=["todo", "in_progress"]
    ).order_by("priority")[:5]
    recent_tasks = (
        Task.objects.filter(author=request.user)
        .exclude(status="done")
        .order_by("-updated_at")[:3]
    )

    # Favoris
    total_bookmarks = Bookmark.objects.filter(author=request.user).count()
    total_collections = (
        Bookmark.objects.filter(author=request.user)
        .values("collection")
        .distinct()
        .count()
    )
    recent_bookmarks = Bookmark.objects.filter(author=request.user).order_by(
        "-created_at"
    )[:3]

    # Articles
    total_articles = Article.objects.filter(author=request.user).count()
    total_published = Article.objects.filter(
        author=request.user, status="published"
    ).count()
    recent_articles = Article.objects.filter(author=request.user).order_by(
        "-updated_at"
    )[:3]

    # Activité 30 jours
    from workspace.models import Log

    logs_30_jours = (
        Log.objects.filter(created_at__gte=trente_jours)
        .extra(select={"day": "date(created_at)"})
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )

    from datetime import timedelta as td

    jours = [(timezone.now() - td(days=i)).date() for i in range(29, -1, -1)]
    logs_par_jour = {str(entry["day"]): entry["total"] for entry in logs_30_jours}
    activite_data = [logs_par_jour.get(str(jour), 0) for jour in jours]
    activite_max = max(activite_data) if activite_data else 1

    # Préférences widgets
    widgets_prefs = request.session.get(
        "dashboard_widgets",
        {
            "today": True,
            "stats": True,
            "tasks": True,
            "bookmarks": True,
            "articles": True,
            "activity": True,
        },
    )

    context = {
        "is_workspace": True,
        "aujourd_hui": aujourd_hui,
        # Notes
        "total_notes": total_notes,
        "notes_semaine": notes_semaine,
        "recent_notes": recent_notes,
        # Tâches
        "total_tasks": total_tasks,
        "tasks_urgent": tasks_urgent,
        "tasks_aujourd_hui": tasks_aujourd_hui,
        "recent_tasks": recent_tasks,
        # Favoris
        "total_bookmarks": total_bookmarks,
        "total_collections": total_collections,
        "recent_bookmarks": recent_bookmarks,
        # Articles
        "total_articles": total_articles,
        "total_published": total_published,
        "recent_articles": recent_articles,
        # Activité
        "activite_data": activite_data,
        "activite_max": activite_max,
        # Widgets
        "widgets": widgets_prefs,
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


def dashboard_widgets(request):
    """Sauvegarde les préférences des widgets du dashboard."""
    if request.method == "POST":
        import json

        data = json.loads(request.body)
        request.session["dashboard_widgets"] = data
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)
