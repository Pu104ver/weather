from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from weather.models import SearchHistory, CityStat
from api.serializers.weather import SearchHistorySerializer, CityStatSerializer

from weather.services import WeatherService


class WeatherView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "city",
                openapi.IN_QUERY,
                description="Название города",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ]
    )
    def get(self, request):
        city = request.query_params.get("city")
        if not city:
            return Response({"detail": "city is required"}, status=400)

        if request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, city=city)
        else:
            session_key = request.session.session_key or request.session.save()
            SearchHistory.objects.create(
                session_key=request.session.session_key, city=city
            )

        data, status = WeatherService.get_weather_data(city)

        return Response(data, status=status)


class UserSearchHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchHistorySerializer

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user).order_by(
            "-searched_at"
        )


class CityStatView(ListAPIView):
    queryset = CityStat.objects.order_by("-count")
    serializer_class = CityStatSerializer
