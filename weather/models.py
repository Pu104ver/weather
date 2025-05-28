from django.db import models
from django.contrib.auth.models import User


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=100)
    city_id = models.BigIntegerField(null=True, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} @ {self.searched_at}"


class CityStat(models.Model):
    city = models.CharField(max_length=100, unique=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.city}: {self.count}"


class City(models.Model):
    geonameid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    asciiname = models.CharField(max_length=200)
    alternatenames = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country_code = models.CharField(max_length=2)
    admin1_code = models.CharField(max_length=30, blank=True)  # регион/штат (поле [10])
    population = models.BigIntegerField()
    timezone = models.CharField(max_length=50, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["asciiname"]),
            models.Index(fields=["country_code"]),
        ]

    def __str__(self):
        location = f"{self.name}, {self.country_code}"
        if self.admin1_code:
            location += f" ({self.admin1_code})"
        return location
