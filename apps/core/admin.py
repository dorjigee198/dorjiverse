from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages as django_messages
from .models import SiteProfile, ContactMessage, Resume


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Your Identity', {
            'fields': ('name', 'tagline', 'bio'),
            'description': 'This is what visitors see on your homepage.'
        }),
        ('Profile Picture', {
            'fields': ('profile_picture', 'profile_preview'),
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url', 'email'),
        }),
    )
    readonly_fields = ['profile_preview']

    def profile_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width:140px;height:140px;object-fit:cover;border-radius:50%;border:3px solid #6366f1;" />',
                obj.profile_picture.url
            )
        return 'No photo uploaded yet.'
    profile_preview.short_description = 'Preview'

    def has_add_permission(self, request):
        # Only allow one profile to exist
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        # Messages come from the public form only
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Add mark-as-read bulk action
        return actions

    actions = ['mark_as_read', 'mark_as_unread']

    @admin.action(description='Mark selected as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='Mark selected as unread')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'active', 'download_link']
    list_editable = ['active']
    ordering = ['-uploaded_at']

    def download_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank" '
                'style="color:#6366f1;font-weight:bold;">⬇ Download</a>',
                obj.file.url
            )
        return '—'
    download_link.short_description = 'File'
