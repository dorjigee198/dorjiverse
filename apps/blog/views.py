from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost, Category, Tag


def blog_list(request):
    posts = BlogPost.objects.filter(
        status=BlogPost.STATUS_PUBLISHED
    ).select_related('category', 'author').prefetch_related('tags')

    categories = Category.objects.all()
    tags = Tag.objects.all()

    query = request.GET.get('q', '').strip()
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query)
        )

    category_slug = request.GET.get('category', '').strip()
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    tag_slug = request.GET.get('tag', '').strip()
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'blog/blog_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'query': query,
        'current_category': category_slug,
        'current_tag': tag_slug,
    })


def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects.select_related('author', 'category').prefetch_related('tags', 'images'),
        slug=slug,
        status=BlogPost.STATUS_PUBLISHED
    )
    related_posts = BlogPost.objects.filter(
        status=BlogPost.STATUS_PUBLISHED,
        category=post.category
    ).exclude(pk=post.pk).order_by('-published_at')[:3]

    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'related_posts': related_posts,
    })
