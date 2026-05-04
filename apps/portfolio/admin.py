from django.contrib import admin
from django.utils.html import format_html
from .models import Skill, Project


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'level', 'order']
    list_editable = ['category', 'level', 'order']
    list_filter = ['category', 'level']
    search_fields = ['name']
    ordering = ['order', 'name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'featured', 'order', 'image_preview',
        'github_link', 'live_demo_link', 'created_at'
    ]
    list_editable = ['featured', 'order']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['featured', 'created_at']
    search_fields = ['title', 'description', 'technologies']
    readonly_fields = ['image_preview', 'created_at']

    fieldsets = (
        ('Project Info', {
            'fields': ('title', 'slug', 'featured', 'order')
        }),
        ('Details', {
            'fields': ('short_description', 'description', 'technologies')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Links', {
            'fields': ('github_link', 'live_demo_link')
        }),
        ('Meta', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:6px;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'
