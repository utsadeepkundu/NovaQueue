from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # The default Django admin site
    path('admin/', admin.site.urls),
    
    # Including the URLs from your 'core' app
    path('', include('core.urls')),
]

# Serving media files (like profile pictures) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)