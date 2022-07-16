from django.shortcuts import render
from django.http import HttpRequest

from .weather_service import WeatherService


def get_current_page(request: HttpRequest):
    weather = WeatherService(request.GET.get('user_id'))
    current = weather.get_current_weather()
    today = weather.get_today_weather()
    return render(request, 'weather/current.html', {'current': current, 'hours': today['weather']})


def get_on_week_page(request):
    weather = WeatherService(request.GET.get('user_id'))
    days = weather.get_days_weather()
    return render(request, 'weather/on_week.html', {'days': days['weather'], 'city_name': days['city_name']})


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip