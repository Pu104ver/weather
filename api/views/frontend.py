from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

from weather.services import WeatherService
from frontend.forms import RegisterForm


def index(request):
    city_name = request.GET.get("city")
    city_id = request.GET.get("city_id")

    weather_data = None
    status_code = None
    
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    last_city = WeatherService.get_last_city(request.user, session_key)
    show_last_city_hint = False

    if not request.session.get("shown_last_city_hint") and last_city and not city_name:
        show_last_city_hint = True
        request.session["shown_last_city_hint"] = True

    if city_name and not city_id:
        weather_data, status_code = WeatherService.get_weather_data_by_city_name(
            city_name=city_name
        )
    if city_id:
        weather_data, status_code = WeatherService.get_weather_data_by_city_id(
            city_id=city_id
        )
    if weather_data and status_code == 200:
        WeatherService.save_search(
            request.user, weather_data["city"], weather_data["id"], session_key
        )
    elif status_code == 404:
        messages.error(request, "Город не найден.")
    elif status_code is not None:
        messages.error(request, f"Произошла ошибка. Код: {status_code}")
     

    unique_history = WeatherService.get_unique_history(request.user, session_key)

    return render(
        request,
        "index.html",
        {
            "weather": weather_data,
            "last_city": last_city,
            "history": unique_history,
            "show_last_city_hint": show_last_city_hint,
        },
    )


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})
