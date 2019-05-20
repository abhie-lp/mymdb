from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("user.urls", namespace="user")),
    path("", include("core.urls", namespace="core")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
