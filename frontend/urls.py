from django.urls import path

from api.views.frontend import index

urlpatterns = [
    path("", index, name="index"),
]
