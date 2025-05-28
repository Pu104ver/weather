import pytest
from django.urls import reverse
from weather.models import SearchHistory
from unittest.mock import patch


@pytest.mark.django_db
@patch("weather.services.WeatherService.get_weather_data_by_city_name")
def test_index_view_get_weather(mock_get_weather_data, client, user):
    mock_get_weather_data.return_value = (
        {
            "city": "Берлин",
            "country": "DE",
            "temp": 15,
            "feels_like": 13,
            "description": "облачно",
            "icon": "02d",
            "wind_speed": 3,
            "pressure": 1015,
            "humidity": 70,
            "id": 2643743,
        },
        200,
    )

    client.force_login(user)
    response = client.get(reverse("index") + "?city=Берлин")
    assert response.status_code == 200
    assert "Берлин".encode("utf-8") in response.content
    assert SearchHistory.objects.filter(user=user, city="Берлин").exists()


@pytest.mark.django_db
def test_index_view_invalid_city(client):
    response = client.get(reverse("index") + "?city=XXXXX")
    assert response.status_code == 200  # страница рендерится, но без данных
    assert (
        "Город не найден".encode("utf-8") in response.content
        or b"weather" not in response.context
    )
