from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),

    # Наш API (все маршруты из issues/urls.py будут доступны по /api/...)
    path('api/', include('issues.urls')),

    # Стандартная авторизация DRF (добавляет кнопку "Log in" в веб-интерфейсе API)
    path('api-auth/', include('rest_framework.urls')),

    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)