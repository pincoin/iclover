from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    path, include
)

urlpatterns = [
    path('minsmine/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('design/', include('design.urls')),
    path('clovi/', include('managing.urls')),
    path('rowapi/', include('api.urls', namespace='rowapi')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
