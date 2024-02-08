from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),

    path('summernote/', include('django_summernote.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += i18n_patterns(
    path('', include('article.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)