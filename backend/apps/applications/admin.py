from django.contrib import admin

from .models import Application, StatusHistory


class HistoryInline(admin.TabularInline):
    model = StatusHistory
    extra = 0
    readonly_fields = ("from_status", "to_status", "changed_at")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("company", "role", "status", "user", "applied_date")
    list_filter = ("status",)
    search_fields = ("company", "role", "user__email")
    inlines = [HistoryInline]
