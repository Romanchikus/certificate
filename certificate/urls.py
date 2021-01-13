
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path('', include('cert_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
           ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf.urls import handler404
from cert_app import views
handler404 = views.handler_404