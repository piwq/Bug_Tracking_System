from django.contrib import admin
from .models import BugReport

@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'priority', 'status', 'reporter', 'created_at')
    list_filter = ('severity', 'priority', 'status')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')