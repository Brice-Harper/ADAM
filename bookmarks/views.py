from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Bookmark, Collection, Tag
from .forms import BookmarkForm, CollectionForm, TagForm
from .utils import fetch_metadata
from workspace.utils import log_action


def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(author=request.user)

    # Filtre par collection
    collection_id = request.GET.get("collection", "")
    if collection_id:
        bookmarks = bookmarks.filter(collection_id=collection_id)

    # Filtre par tag
    tag_id = request.GET.get("tag", "")
    if tag_id:
        bookmarks = bookmarks.filter(tags__id=tag_id)

    # Recherche globale
    query = request.GET.get("q", "")
    if query:
        bookmarks = bookmarks.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(url__icontains=query)
        )

    collections = Collection.objects.filter(author=request.user)
    tags = Tag.objects.filter(author=request.user)

    # Stats
    total = Bookmark.objects.filter(author=request.user).count()
    total_collections = collections.count()
    total_tags = tags.count()

    context = {
        "is_workspace": True,
        "bookmarks": bookmarks,
        "collections": collections,
        "tags": tags,
        "collection_id": collection_id,
        "tag_id": tag_id,
        "query": query,
        "total": total,
        "total_collections": total_collections,
        "total_tags": total_tags,
    }
    return render(request, "bookmarks/bookmark_list.html", context)


def bookmark_create(request):
    if request.method == "POST":
        form = BookmarkForm(request.POST, user=request.user)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.author = request.user
            bookmark.save()
            form.save_m2m()
            log_action(request.user, "bookmark_create", bookmark.title)
            messages.success(request, "Favori ajouté avec succès")
            return redirect("bookmark_list")
    else:
        form = BookmarkForm(user=request.user)

    context = {
        "is_workspace": True,
        "form": form,
        "page_title": "Ajouter un favori",
        "submit_label": "Ajouter",
    }
    return render(request, "bookmarks/bookmark_form.html", context)


def bookmark_detail(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id, author=request.user)
    context = {
        "is_workspace": True,
        "bookmark": bookmark,
    }
    return render(request, "bookmarks/bookmark_detail.html", context)


def bookmark_update(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id, author=request.user)

    if request.method == "POST":
        form = BookmarkForm(request.POST, instance=bookmark, user=request.user)
        if form.is_valid():
            form.save()
            log_action(request.user, "bookmark_update", bookmark.title)
            messages.success(request, "Favori mis à jour avec succès")
            return redirect("bookmark_detail", bookmark_id=bookmark.id)
    else:
        form = BookmarkForm(instance=bookmark, user=request.user)

    selected_tag_ids = list(bookmark.tags.values_list("id", flat=True))

    context = {
        "is_workspace": True,
        "form": form,
        "bookmark": bookmark,
        "page_title": "Modifier le favori",
        "submit_label": "Mettre à jour",
        "selected_tag_ids": selected_tag_ids,
    }
    return render(request, "bookmarks/bookmark_form.html", context)


def bookmark_delete(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id, author=request.user)

    if request.method == "POST":
        log_action(request.user, "bookmark_delete", bookmark.title)
        bookmark.delete()
        messages.success(request, "Favori supprimé avec succès")
        return redirect("bookmark_list")

    context = {
        "is_workspace": True,
        "bookmark": bookmark,
    }
    return render(request, "bookmarks/bookmark_confirm_delete.html", context)


def fetch_metadata_view(request):
    """
    Vue AJAX qui récupère les métadonnées d'une URL.
    """
    url = request.GET.get("url", "")
    if not url:
        return JsonResponse({"error": "URL manquante"}, status=400)

    metadata = fetch_metadata(url)
    return JsonResponse(metadata)


def collection_list(request):
    collections = Collection.objects.filter(author=request.user)
    form = CollectionForm()

    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.author = request.user
            collection.save()
            messages.success(request, "Collection créée avec succès")
            return redirect("collection_list")

    context = {
        "is_workspace": True,
        "collections": collections,
        "form": form,
    }
    return render(request, "bookmarks/collection_list.html", context)


def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id, author=request.user)
    bookmarks = Bookmark.objects.filter(author=request.user, collection=collection)
    context = {
        "is_workspace": True,
        "collection": collection,
        "bookmarks": bookmarks,
    }
    return render(request, "bookmarks/collection_detail.html", context)


def collection_update(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id, author=request.user)

    if request.method == "POST":
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            messages.success(request, "Collection mise à jour avec succès")
            return redirect("collection_list")
    else:
        form = CollectionForm(instance=collection)

    context = {
        "is_workspace": True,
        "form": form,
        "collection": collection,
    }
    return render(request, "bookmarks/collection_update.html", context)


def collection_delete(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id, author=request.user)

    if request.method == "POST":
        collection.delete()
        messages.success(request, "Collection supprimée avec succès")
        return redirect("collection_list")

    context = {
        "is_workspace": True,
        "collection": collection,
    }
    return render(request, "bookmarks/collection_confirm_delete.html", context)


def tag_list(request):
    tags = Tag.objects.filter(author=request.user)
    form = TagForm()

    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.author = request.user
            tag.save()
            messages.success(request, "Tag créé avec succès")
            return redirect("tag_list")

    context = {
        "is_workspace": True,
        "tags": tags,
        "form": form,
    }
    return render(request, "bookmarks/tag_list.html", context)


def tag_delete(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, author=request.user)

    if request.method == "POST":
        tag.delete()
        messages.success(request, "Tag supprimé avec succès")
        return redirect("tag_list")

    context = {
        "is_workspace": True,
        "tag": tag,
    }
    return render(request, "bookmarks/tag_confirm_delete.html", context)
