from rest_framework import serializers
from .models import BugReport

class BugReportSerializer(serializers.ModelSerializer):
    # Добавляем поле, чтобы видеть имя репортера, а не только его ID
    reporter_username = serializers.ReadOnlyField(source='reporter.username')
    assignee_username = serializers.ReadOnlyField(source='assignee.username')

    class Meta:
        model = BugReport
        fields = '__all__' # Включаем все поля
        # Эти поля нельзя менять вручную через API (они ставятся автоматом)
        read_only_fields = ('reporter', 'created_at', 'updated_at')