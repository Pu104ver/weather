from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(title="Weather API", default_version="v1"),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path('', include('frontend.urls')),
]


