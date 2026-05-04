from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin panel branding
admin.site.site_header = 'Dorjivers Admin'
admin.site.site_title = 'Dorjivers'
admin.site.index_title = 'Welcome to Dorjivers Admin Panel'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('apps.core.urls', namespace='core')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('portfolio/', include('apps.portfolio.urls', namespace='portfolio')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
