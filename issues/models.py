from django.db import models
from django.conf import settings  # Импортируем настройки, чтобы ссылаться на модель User


class BugReport(models.Model):
    # --- Справочники (Choices) согласно скрину ---
    class Severity(models.TextChoices):
        BLOCKER = 'S1', 'S1 (Blocker) - Блокирует работу'
        CRITICAL = 'S2', 'S2 (Critical) - Крит. бизнес-логика'
        MAJOR = 'S3', 'S3 (Major) - Нарушает функционал'
        MINOR = 'S4', 'S4 (Minor) - Незначительная ошибка UI'
        TRIVIAL = 'S5', 'S5 (Trivial) - Опечатка/мелочь'

    class Priority(models.TextChoices):
        HIGH = 'P1', 'P1 (High) - Исправить немедленно'
        MEDIUM = 'P2', 'P2 (Medium) - Ближайший релиз'
        LOW = 'P3', 'P3 (Low) - Может ждать'

    class Status(models.TextChoices):
        NEW = 'NEW', 'Новый'
        IN_PROGRESS = 'IN_PROGRESS', 'В работе'
        FIXED = 'FIXED', 'Исправлен'
        CLOSED = 'CLOSED', 'Закрыт'

    # --- Поля модели ---
    title = models.CharField(max_length=255, verbose_name="Заголовок")

    severity = models.CharField(
        max_length=2,
        choices=Severity.choices,
        default=Severity.MAJOR,
        verbose_name="Серьезность"
    )

    priority = models.CharField(
        max_length=2,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="Приоритет"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус"
    )

    # Текстовые поля (Textarea)
    environment = models.TextField(verbose_name="Окружение (OS, Browser)")
    preconditions = models.TextField(blank=True, verbose_name="Предусловие")
    steps_to_reproduce = models.TextField(verbose_name="Шаги воспроизведения")
    expected_result = models.TextField(verbose_name="Ожидаемый результат")
    actual_result = models.TextField(verbose_name="Фактический результат")

    # Файлы (скриншоты, логи)
    attachment = models.FileField(upload_to='bugs/', blank=True, null=True, verbose_name="Вложение")

    # Кто создал и на ком висит
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reported_bugs',
        verbose_name="Репортер"
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_bugs',
        verbose_name="Исполнитель"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = 'Баг-репорт'
        verbose_name_plural = 'Баг-репорты'
        ordering = ['-created_at']  # Свежие баги сверху

    def __str__(self):
        return f"[{self.severity}] {self.title}"