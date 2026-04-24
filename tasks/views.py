from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta, date
import json

from .models import Task, SubTask, Category, Label
from .forms import TaskForm, SubTaskForm, CategoryForm, LabelForm
from workspace.utils import log_action


def task_list(request):
    tasks = Task.objects.filter(author=request.user).order_by("order", "due_date")

    # Filtres
    status_filter = request.GET.get("status", "")
    priority_filter = request.GET.get("priority", "")
    category_filter = request.GET.get("category", "")

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if category_filter:
        tasks = tasks.filter(category_id=category_filter)

    # Sections intelligentes
    aujourd_hui = date.today()
    fin_semaine = aujourd_hui + timedelta(days=7)

    tasks_en_retard = tasks.filter(
        due_date__lt=aujourd_hui, status__in=["todo", "in_progress"]
    )
    tasks_aujourd_hui = tasks.filter(
        due_date=aujourd_hui, status__in=["todo", "in_progress"]
    )
    tasks_semaine = tasks.filter(
        due_date__gt=aujourd_hui,
        due_date__lte=fin_semaine,
        status__in=["todo", "in_progress"],
    )

    # Stats
    total = Task.objects.filter(author=request.user).count()
    total_done = Task.objects.filter(author=request.user, status="done").count()
    total_urgent = Task.objects.filter(
        author=request.user, priority="urgent", status__in=["todo", "in_progress"]
    ).count()

    categories = Category.objects.filter(author=request.user)

    context = {
        "is_workspace": True,
        "tasks": tasks,
        "tasks_en_retard": tasks_en_retard,
        "tasks_aujourd_hui": tasks_aujourd_hui,
        "tasks_semaine": tasks_semaine,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "category_filter": category_filter,
        "status_choices": Task.STATUS_CHOICES,
        "priority_choices": Task.PRIORITY_CHOICES,
        "categories": categories,
        "total": total,
        "total_done": total_done,
        "total_urgent": total_urgent,
    }
    return render(request, "tasks/task_list.html", context)


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            log_action(request.user, "task_create", task.title)
            messages.success(request, "Tâche créée avec succès")
            return redirect("task_list")
    else:
        form = TaskForm(user=request.user)

    context = {
        "is_workspace": True,
        "form": form,
        "page_title": "Créer une tâche",
        "submit_label": "Créer",
    }
    return render(request, "tasks/task_form.html", context)


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    subtasks = task.subtasks.all()
    subtask_form = SubTaskForm()

    if request.method == "POST":
        subtask_form = SubTaskForm(request.POST)
        if subtask_form.is_valid():
            subtask = subtask_form.save(commit=False)
            subtask.task = task
            subtask.order = subtasks.count()
            subtask.save()
            messages.success(request, "Sous-tâche ajoutée avec succès")
            return redirect("task_detail", task_id=task.id)

    context = {
        "is_workspace": True,
        "task": task,
        "subtasks": subtasks,
        "subtask_form": subtask_form,
    }
    return render(request, "tasks/task_detail.html", context)


def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            log_action(request.user, "task_update", task.title)
            messages.success(request, "Tâche mise à jour avec succès")
            return redirect("task_detail", task_id=task.id)
    else:
        form = TaskForm(instance=task, user=request.user)

    selected_labels_ids = list(task.labels.values_list("id", flat=True))

    context = {
        "is_workspace": True,
        "form": form,
        "task": task,
        "page_title": "Modifier la tâche",
        "submit_label": "Mettre à jour",
        "selected_label_ids": selected_labels_ids,
    }
    return render(request, "tasks/task_form.html", context)


def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)

    if request.method == "POST":
        log_action(request.user, "task_delete", task.title)
        task.delete()
        messages.success(request, "Tâche supprimée avec succès")
        return redirect("task_list")

    context = {
        "is_workspace": True,
        "task": task,
    }
    return render(request, "tasks/task_confirm_delete.html", context)


@require_POST
def task_toggle(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    if task.status == "done":
        task.status = "todo"
    else:
        task.status = "done"
    task.save()
    log_action(
        request.user,
        "task_update",
        f"{task.title} — statut : {task.get_status_display()}",
    )
    return JsonResponse({"status": task.status, "label": task.get_status_display()})


@require_POST
def task_reorder(request):
    try:
        data = json.loads(request.body)
        for item in data:
            Task.objects.filter(id=item["id"], author=request.user).update(
                order=item["order"]
            )
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


def category_list(request):
    categories = Category.objects.filter(author=request.user)
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.author = request.user
            category.save()
            messages.success(request, "Catégorie créée avec succès")
            return redirect("category_list")

    context = {
        "is_workspace": True,
        "categories": categories,
        "form": form,
    }
    return render(request, "tasks/category_list.html", context)


def category_create(request):
    return redirect("category_list")


def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id, author=request.user)

    if request.method == "POST":
        category.delete()
        messages.success(request, "Catégorie supprimée avec succès")
        return redirect("category_list")

    context = {
        "is_workspace": True,
        "category": category,
    }
    return render(request, "tasks/category_confirm_delete.html", context)


def label_list(request):
    labels = Label.objects.filter(author=request.user)
    form = LabelForm()

    if request.method == "POST":
        form = LabelForm(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            label.author = request.user
            label.save()
            messages.success(request, "Étiquette créée avec succès")
            return redirect("label_list")

    context = {
        "is_workspace": True,
        "labels": labels,
        "form": form,
    }
    return render(request, "tasks/label_list.html", context)


def label_create(request):
    return redirect("label_list")


def label_delete(request, label_id):
    label = get_object_or_404(Label, id=label_id, author=request.user)

    if request.method == "POST":
        label.delete()
        messages.success(request, "Étiquette supprimée avec succès")
        return redirect("label_list")

    context = {
        "is_workspace": True,
        "label": label,
    }
    return render(request, "tasks/label_confirm_delete.html", context)


@require_POST
def subtask_toggle(request, task_id, subtask_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    subtask = get_object_or_404(SubTask, id=subtask_id, task=task)
    subtask.is_done = not subtask.is_done
    subtask.save()
    return JsonResponse({"is_done": subtask.is_done})


def subtask_update(request, task_id, subtask_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    subtask = get_object_or_404(SubTask, id=subtask_id, task=task)

    if request.method == "POST":
        form = SubTaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            messages.success(request, "Sous-tâche mise à jour avec succès")
            return redirect("task_detail", task_id=task.id)
    else:
        form = SubTaskForm(instance=subtask)

    context = {
        "is_workspace": True,
        "form": form,
        "task": task,
        "subtask": subtask,
    }
    return render(request, "tasks/subtask_form.html", context)


@require_POST
def subtask_delete(request, task_id, subtask_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    subtask = get_object_or_404(SubTask, id=subtask_id, task=task)
    subtask.delete()
    messages.success(request, "Sous-tâche supprimée avec succès")
    return redirect("task_detail", task_id=task.id)


def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id, author=request.user)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie mise à jour avec succès")
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)

    context = {
        "is_workspace": True,
        "form": form,
        "category": category,
    }
    return render(request, "tasks/category_update.html", context)


def label_update(request, label_id):
    label = get_object_or_404(Label, id=label_id, author=request.user)

    if request.method == "POST":
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, "Étiquette mise à jour avec succès")
            return redirect("label_list")
    else:
        form = LabelForm(instance=label)

    context = {
        "is_workspace": True,
        "form": form,
        "label": label,
    }
    return render(request, "tasks/label_update.html", context)
