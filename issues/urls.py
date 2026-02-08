from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BugReportViewSet

# Создаем роутер и регистрируем наш ViewSet
router = DefaultRouter()
router.register(r'bugs', BugReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
