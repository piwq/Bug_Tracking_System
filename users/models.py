from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Определяем роли через TextChoices (это современный и удобный способ в Django)
    class Role(models.TextChoices):
        QA = 'QA', 'QA Engineer'      # Тестировщик
        DEV = 'DEV', 'Developer'      # Разработчик
        ADMIN = 'ADMIN', 'Admin'      # Админ/Менеджер

    # Добавляем поле роли к стандартному пользователю
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.QA,
        verbose_name='Роль'
    )

    # Можно добавить поле "Telegram ID", если захочешь потом уведомления в телегу
    telegram_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Telegram ID')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"