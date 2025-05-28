from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.db.models import Q, Max

from weather.models import CityStat, SearchHistory

import requests
import os

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


class WeatherService:
    @staticmethod
    def get_weather_data(city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&lang=ru&units=metric"

        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return None, response.status_code

            data = response.json()

            weather_data = {
                "city": data.get("name"),
                "country": data["sys"].get("country"),
                "temp": data["main"].get("temp"),
                "feels_like": data["main"].get("feels_like"),
                "description": data["weather"][0].get("description") if data.get("weather") else None,
                "icon": data["weather"][0].get("icon") if data.get("weather") else None,
                "wind_speed": data["wind"].get("speed"),
                "pressure": data["main"].get("pressure"),
                "humidity": data["main"].get("humidity"),
            }

            stat, _ = CityStat.objects.get_or_create(city=weather_data["city"])
            stat.count += 1
            stat.save()

            return weather_data, 200

        except requests.RequestException:
            return None, 503
        except (KeyError, TypeError, ValueError):
            return None, 500


    @staticmethod
    def get_user_filter(user: User, session_key=None):
        if user.is_authenticated:
            return Q(user=user)
        return Q(session_key=session_key, user__isnull=True)

    @staticmethod
    def save_search(user: User, city, session_key=None):
        filter_kwargs = {}
        if user.is_authenticated:
            SearchHistory.objects.filter(user__isnull=True, session_key=session_key).update(user=user)
            filter_kwargs["user"] = user
        else:
            filter_kwargs["session_key"] = session_key

        SearchHistory.objects.create(city=city, **filter_kwargs)

    @staticmethod
    def get_last_city(user, session_key=None):
        user_filter = WeatherService.get_user_filter(user, session_key)
        last_entry = (
            SearchHistory.objects.filter(user_filter).order_by("-searched_at").first()
        )
        return last_entry.city if last_entry else None

    @staticmethod
    def get_unique_history(user, session_key=None):
        user_filter = WeatherService.get_user_filter(user, session_key)
        latest = (
            SearchHistory.objects.filter(user_filter)
            .values("city")
            .annotate(latest_time=Max("searched_at"))
            .order_by("-latest_time")
        )
        return SearchHistory.objects.filter(
            user_filter,
            searched_at__in=[x["latest_time"] for x in latest],
            city__in=[x["city"] for x in latest],
        ).order_by("-searched_at")
