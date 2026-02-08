from rest_framework import viewsets, permissions, status
from .models import BugReport
from .serializers import BugReportSerializer
from .permissions import IsQAOrReadOnly, IsReporterOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .ai_service import suggest_bug_title

class BugReportViewSet(viewsets.ModelViewSet):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer

    # Настройка прав доступа
    # Сейчас стоит: Только авторизованные пользователи могут что-то делать
    permission_classes = [permissions.IsAuthenticated]

    # Метод, который срабатывает при создании бага
    def perform_create(self, serializer):
        # Автоматически назначаем текущего юзера как репортера
        serializer.save(reporter=self.request.user)


class AISuggestTitleView(APIView):
    def post(self, request):
        raw_text = request.data.get('text', '')

        if not raw_text:
            return Response({"error": "Текст не передан"}, status=status.HTTP_400_BAD_REQUEST)

        # Вся магия происходит в сервисе
        suggested_title = suggest_bug_title(raw_text)

        return Response({"suggested": suggested_title})