from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin
from .models import Category, Tag, BlogPost, BlogImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = '# Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = '# Posts'


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 2
    fields = ['image', 'caption']


@admin.register(BlogPost)
class BlogPostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

    list_display = [
        'title', 'author', 'category', 'status',
        'published_at', 'featured_image_preview'
    ]
    list_filter = ['status', 'category', 'tags', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at', 'featured_image_preview']
    inlines = [BlogImageInline]

    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Media & Content', {
            'fields': ('featured_image', 'featured_image_preview', 'excerpt', 'content')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at'),
            'description': 'Set status to Published and save to make the post live.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:8px;" />',
                obj.featured_image.url
            )
        return '—'
    featured_image_preview.short_description = 'Preview'


@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'caption', 'uploaded_at']
    list_filter = ['post']
