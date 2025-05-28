from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib.auth.views import LoginView, LogoutView

from api.views.weather import WeatherView, UserSearchHistoryView, CityStatView, autocomplete_city
from api.views.frontend import register_view


schema_view = get_schema_view(
    openapi.Info(title="Weather API", default_version="v1"),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("weather/", WeatherView.as_view(), name="weather"),
    path("history/", UserSearchHistoryView.as_view(), name="user-history"),
    path("stats/", CityStatView.as_view(), name="city-stats"),
    path("autocomplete-city/", autocomplete_city, name="autocomplete_city"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", register_view, name="register"),
]
