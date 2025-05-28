from django.contrib import admin
from .models import SearchHistory, CityStat


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "session_key", "city", "searched_at")
    list_filter = ("city", "searched_at")
    search_fields = ("user__username", "city", "session_key")


@admin.register(CityStat)
class CityStatAdmin(admin.ModelAdmin):
    list_display = ("city", "count")
    ordering = ("-count",)
    search_fields = ("city",)
