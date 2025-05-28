from django.contrib import admin
from .models import SearchHistory, CityStat, City


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


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country_code",
        "admin1_code",
        "population",
        "latitude",
        "longitude",
    )
    search_fields = ("name", "asciiname", "alternatenames", "country_code")
    list_filter = ("country_code",)
    ordering = ("-population", "name")
    readonly_fields = ("geonameid",)
    fieldsets = (
        (None, {"fields": ("geonameid", "name", "admin1_code", "asciiname", "alternatenames")}),
        ("Географические данные", {"fields": ("latitude", "longitude")}),
        ("Дополнительные данные", {"fields": ("country_code", "population", "timezone")}),
    )
