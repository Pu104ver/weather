from django.db import models
from django.contrib.auth.models import User


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=100)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} @ {self.searched_at}"


class CityStat(models.Model):
    city = models.CharField(max_length=100, unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.city}: {self.count}"
