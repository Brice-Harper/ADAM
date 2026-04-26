from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article, Category, Tag


def blog_home(request):
    articles = Article.objects.filter(status="published").order_by("-published_at")

    # Filtres
    category_slug = request.GET.get("category", "")
    tag_slug = request.GET.get("tag", "")
    query = request.GET.get("q", "")

    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    if tag_slug:
        articles = articles.filter(tags__slug=tag_slug)
    if query:
        articles = articles.filter(title__icontains=query)

    # Pagination
    paginator = Paginator(articles, 9)
    page_number = request.GET.get("page")
    articles = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()
    selected_category = (
        Category.objects.filter(slug=category_slug).first() if category_slug else None
    )
    selected_tag = Tag.objects.filter(slug=tag_slug).first() if tag_slug else None

    context = {
        "articles": articles,
        "categories": categories,
        "tags": tags,
        "query": query,
        "category_slug": category_slug,
        "tag_slug": tag_slug,
        "selected_category": selected_category,
        "selected_tag": selected_tag,
    }
    return render(request, "blog/public/blog_home.html", context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status="published")

    # Articles similaires — même catégorie, excluant l'article actuel
    related_articles = (
        Article.objects.filter(status="published", category=article.category)
        .exclude(id=article.id)
        .order_by("-published_at")[:3]
    )

    context = {
        "article": article,
        "related_articles": related_articles,
    }
    return render(request, "blog/public/article_detail.html", context)


def blog_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(status="published", category=category).order_by(
        "-published_at"
    )

    paginator = Paginator(articles, 9)
    page_number = request.GET.get("page")
    articles = paginator.get_page(page_number)

    context = {
        "category": category,
        "articles": articles,
    }
    return render(request, "blog/public/blog_category.html", context)


def blog_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(status="published", tags=tag).order_by(
        "-published_at"
    )

    paginator = Paginator(articles, 9)
    page_number = request.GET.get("page")
    articles = paginator.get_page(page_number)

    context = {
        "tag": tag,
        "articles": articles,
    }
    return render(request, "blog/public/blog_tag.html", context)
