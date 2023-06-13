from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("index.urls")),
    path("authentication/", include("authentication.urls")),
    path("userprofile/", include("userprofile.urls")),
    path("friends/", include("friends.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
