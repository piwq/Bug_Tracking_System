from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Расширяем стандартную админку, чтобы видеть поле 'role'
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'telegram_id')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')