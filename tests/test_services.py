import pytest
from weather.models import SearchHistory, CityStat
from weather.services import WeatherService
from unittest.mock import patch


@pytest.mark.django_db
def test_save_search_with_authenticated_user(user):
    WeatherService.save_search(user, "Москва", session_key="test")
    assert SearchHistory.objects.filter(user=user, city="Москва").exists()


@pytest.mark.django_db
def test_save_search_with_session_key():
    WeatherService.save_search(user=None, city="Париж", session_key="abc123")
    assert SearchHistory.objects.filter(session_key="abc123", city="Париж").exists()


@pytest.mark.django_db
@patch("weather.services.requests.get")
def test_get_weather_data_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "name": "Лондон",
        "sys": {"country": "GB"},
        "main": {"temp": 10, "feels_like": 8, "pressure": 1012, "humidity": 60},
        "weather": [{"description": "ясно", "icon": "01d"}],
        "wind": {"speed": 4},
    }

    data, status = WeatherService.get_weather_data_by_city_name("Лондон")
    assert status == 200
    assert data["city"] == "Лондон"
    assert CityStat.objects.filter(city="Лондон").exists()


@pytest.mark.django_db
@patch("weather.services.requests.get")
def test_get_weather_data_failure(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"message": "city not found"}

    data, status = WeatherService.get_weather_data_by_city_name("Неизвестный")
    assert status == 404
    assert data is None
