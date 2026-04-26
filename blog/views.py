from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Article, Category, Tag
from .forms import ArticleForm, CategoryForm, TagForm
from workspace.utils import log_action


def article_list(request):
    articles = Article.objects.filter(author=request.user).order_by("-created_at")

    # Filtres
    status_filter = request.GET.get("status", "")
    category_filter = request.GET.get("category", "")
    query = request.GET.get("q", "")

    if status_filter:
        articles = articles.filter(status=status_filter)
    if category_filter:
        articles = articles.filter(category_id=category_filter)
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query)
        )

    categories = Category.objects.all()

    # Stats
    total = Article.objects.filter(author=request.user).count()
    total_published = Article.objects.filter(
        author=request.user, status="published"
    ).count()
    total_draft = Article.objects.filter(author=request.user, status="draft").count()

    context = {
        "is_workspace": True,
        "articles": articles,
        "categories": categories,
        "status_filter": status_filter,
        "category_filter": category_filter,
        "query": query,
        "status_choices": Article.STATUS_CHOICES,
        "total": total,
        "total_published": total_published,
        "total_draft": total_draft,
    }
    return render(request, "blog/article_list.html", context)


def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()
            log_action(request.user, "article_create", article.title)
            messages.success(request, "Article créé avec succès")
            return redirect("article_list")
    else:
        form = ArticleForm()

    selected_tag_ids = []
    context = {
        "is_workspace": True,
        "form": form,
        "page_title": "Créer un article",
        "submit_label": "Créer",
        "selected_tag_ids": selected_tag_ids,
    }
    return render(request, "blog/article_form.html", context)


def article_update(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            log_action(request.user, "article_update", article.title)
            messages.success(request, "Article mis à jour avec succès")
            return redirect("article_list")
    else:
        form = ArticleForm(instance=article)

    selected_tag_ids = list(article.tags.values_list("id", flat=True))

    context = {
        "is_workspace": True,
        "form": form,
        "article": article,
        "page_title": "Modifier l'article",
        "submit_label": "Mettre à jour",
        "selected_tag_ids": selected_tag_ids,
    }
    return render(request, "blog/article_form.html", context)


def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)

    if request.method == "POST":
        log_action(request.user, "article_delete", article.title)
        article.delete()
        messages.success(request, "Article supprimé avec succès")
        return redirect("article_list")

    context = {
        "is_workspace": True,
        "article": article,
    }
    return render(request, "blog/article_confirm_delete.html", context)


def article_preview(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)
    context = {
        "article": article,
        "is_preview": True,
    }
    return render(request, "blog/public/article_detail.html", context)


def blog_category_list(request):
    categories = Category.objects.all()
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie créée avec succès")
            return redirect("blog_category_list")

    context = {
        "is_workspace": True,
        "categories": categories,
        "form": form,
    }
    return render(request, "blog/category_list.html", context)


def blog_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.delete()
        messages.success(request, "Catégorie supprimée avec succès")
        return redirect("blog_category_list")

    context = {
        "is_workspace": True,
        "category": category,
    }
    return render(request, "blog/category_confirm_delete.html", context)


def blog_tag_list(request):
    tags = Tag.objects.all()
    form = TagForm()

    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tag créé avec succès")
            return redirect("blog_tag_list")

    context = {
        "is_workspace": True,
        "tags": tags,
        "form": form,
    }
    return render(request, "blog/tag_list.html", context)


def blog_tag_delete(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)

    if request.method == "POST":
        tag.delete()
        messages.success(request, "Tag supprimé avec succès")
        return redirect("blog_tag_list")

    context = {
        "is_workspace": True,
        "tag": tag,
    }
    return render(request, "blog/tag_confirm_delete.html", context)
